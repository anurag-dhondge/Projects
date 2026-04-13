import sys
import os
import time
import uuid
import threading
import traceback

# Ensure current directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
from dotenv import load_dotenv
from config import UPLOAD_FOLDER, OUTPUT_FOLDER, VIDEO_EXTENSIONS
from vision_utils.file_utils import allowed_file, save_file
from generative.text_to_image import generate_from_text, get_pipe
from generative.image_to_image import generate_from_image
from generative.sketch_to_image import generate_from_sketch, get_sketch_pipe
from processing.detection import detect_objects
from processing.recognition import recognize_image
from processing.restoration import restore_image, compute_diff_visual
from processing.video import restore_video
from processing.enhancement import enhance_image
from processing.deep_deblur import run_deblurgan_and_save, pick_default_deblurgan_model

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ── Always return JSON errors — never return Werkzeug HTML debug pages ──────
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"[ERROR] Unhandled exception: {e}", flush=True)
    traceback.print_exc()
    code = getattr(e, 'code', 500)
    if not isinstance(code, int):
        code = 500
    return jsonify({"error": str(e)}), code

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

_jobs = {}
_jobs_lock = threading.Lock()


def _job_set(job_id: str, **updates):
    with _jobs_lock:
        if job_id not in _jobs:
            return
        _jobs[job_id].update(updates)


def _job_get(job_id: str):
    with _jobs_lock:
        return _jobs.get(job_id)


# ── Warm up generative pipelines on startup (sequential to avoid OOM) ───────
try:
    def _warmup_all():
        try:
            print("[startup] Warming up text-to-image pipeline...", flush=True)
            get_pipe()
            print("[startup] Text-to-image pipeline ready.", flush=True)
        except Exception as e:
            print(f"[startup] Warmup failed: {e}", flush=True)
            traceback.print_exc()
        try:
            print("[startup] Warming up sketch-to-image pipeline...", flush=True)
            get_sketch_pipe()
            print("[startup] Sketch-to-image pipeline ready.", flush=True)
        except Exception as e:
            print(f"[startup] Sketch warmup failed: {e}", flush=True)
            traceback.print_exc()

    threading.Thread(target=_warmup_all, daemon=True).start()
except Exception:
    pass


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index_page():
    return redirect("http://localhost:3000", code=302)


@app.route("/api/health")
def api_health():
    return jsonify({"status": "ok"})


@app.route("/api/capabilities")
def api_capabilities():
    tf_ok = False
    try:
        import tensorflow  # noqa: F401
        tf_ok = True
    except Exception:
        tf_ok = False

    model_ok = False
    try:
        mp = pick_default_deblurgan_model()
        if mp and os.path.exists(mp):
            with open(mp, "rb") as f:
                sig = f.read(8)
            model_ok = sig == b"\x89HDF\r\n\x1a\n"
    except Exception:
        model_ok = False

    return jsonify({"deblurgan_v2": bool(tf_ok and model_ok)})


@app.route("/api/job/start", methods=["POST"])
def api_job_start():
    action = request.form.get("action", "").strip()
    if action not in ("generate_text", "sketch_to_image"):
        return jsonify({"error": "Invalid action"}), 400

    prompt = request.form.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    width = int(request.form.get("width", 512) or 512)
    height = int(request.form.get("height", 512) or 512)
    steps = int(request.form.get("steps", 25) or 25)

    file = request.files.get("image")
    input_path = None
    if action == "sketch_to_image":
        if not file:
            return jsonify({"error": "No image provided"}), 400
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400
        input_path = save_file(file, UPLOAD_FOLDER)

    job_id = uuid.uuid4().hex
    now = time.time()
    with _jobs_lock:
        _jobs[job_id] = {
            "id": job_id,
            "action": action,
            "status": "queued",
            "step": 0,
            "total": steps,
            "elapsed_s": 0.0,
            "eta_s": None,
            "created_at": now,
            "started_at": None,
            "finished_at": None,
            "output_path": None,
            "error": None,
            "input_path": input_path,
        }

    def _run_job():
        try:
            _job_set(job_id, status="running", started_at=time.time())

            def _progress_cb(step: int, total: int, elapsed_s: float):
                eta_s = None
                if step and elapsed_s > 0:
                    sps = float(step) / float(elapsed_s)
                    if sps > 0:
                        eta_s = float(total - step) / sps
                _job_set(job_id, step=int(step), total=int(total),
                         elapsed_s=float(elapsed_s), eta_s=eta_s)

            if action == "generate_text":
                out_path = generate_from_text(
                    prompt, OUTPUT_FOLDER,
                    width=width, height=height,
                    steps=steps, progress_cb=_progress_cb,
                )
                _job_set(job_id, output_path=out_path)
            else:
                assert input_path is not None
                out_path = generate_from_sketch(
                    input_path, prompt, OUTPUT_FOLDER,
                    width=width, height=height,
                    steps=steps, progress_cb=_progress_cb,
                )
                _job_set(job_id, output_path=out_path)

            _job_set(job_id, status="done", finished_at=time.time())
        except Exception as e:
            _job_set(job_id, status="error", error=str(e), finished_at=time.time())

    threading.Thread(target=_run_job, daemon=True).start()
    return jsonify({"job_id": job_id})


@app.route("/api/job/<job_id>")
def api_job_status(job_id: str):
    job = _job_get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    output_url = None
    if job.get("output_path"):
        out_name = os.path.basename(job["output_path"])
        output_url = f"/outputs/{out_name}"

    original_url = None
    if job.get("input_path"):
        orig_name = os.path.basename(job["input_path"])
        original_url = f"/uploads/{orig_name}"

    return jsonify({
        "job_id": job["id"],
        "action": job["action"],
        "status": job["status"],
        "step": job.get("step", 0),
        "total": job.get("total", 0),
        "elapsed_s": job.get("elapsed_s", 0.0),
        "eta_s": job.get("eta_s"),
        "error": job.get("error"),
        "output_url": output_url,
        "original_url": original_url,
    })


@app.route("/api/process", methods=["POST"])
def api_process():
    action = request.form.get("action", "").strip()
    if not action:
        return jsonify({"error": "No action provided"}), 400

    file = request.files.get("image")
    prompt = request.form.get("prompt", "").strip()

    # ── Image analysis actions ───────────────────────────────────────────────
    if action in ("restore", "enhance", "detect", "recognize"):
        if not file:
            return jsonify({"error": "No image provided"}), 400
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400
        try:
            input_path = save_file(file, UPLOAD_FOLDER)
            overlay_path = None
            mask_path = None
            classes = None

            if action == "restore":
                strength = request.form.get("strength", "medium").strip().lower()
                enhance_after = request.form.get("enhance_after", "false").strip().lower() in ("1", "true", "yes", "on")
                engine = request.form.get("engine", "rl").strip().lower()
                filename = os.path.basename(input_path)
                ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
                is_video = ext in VIDEO_EXTENSIONS

                if engine == "deblurgan" and not is_video:
                    model_path = request.form.get("model_path", "").strip() or None
                    try:
                        output_path = run_deblurgan_and_save(input_path, OUTPUT_FOLDER, model_path)
                    except RuntimeError as e:
                        return jsonify({"error": f"DeblurGAN-v2 error: {e}"}), 400
                else:
                    blur_type = request.form.get("blur_type", "auto").strip().lower()
                    motion_length = int(request.form.get("motion_length", 9) or 9)
                    motion_angle = float(request.form.get("motion_angle", 0.0) or 0.0)
                    denoise_before = request.form.get("denoise_before", "false").strip().lower() in ("1", "true", "yes", "on")
                    extra_iters = int(request.form.get("extra_iters", 0) or 0)
                    derain_before = request.form.get("derain_before", "false").strip().lower() in ("1", "true", "yes", "on")

                    if is_video:
                        output_path = restore_video(
                            input_path, OUTPUT_FOLDER,
                            strength=strength, enhance_after=enhance_after,
                            blur_type=blur_type, motion_length=motion_length,
                            motion_angle=motion_angle, denoise_before=denoise_before,
                            extra_iters=extra_iters, derain_before=derain_before,
                        )
                    else:
                        output_path = restore_image(
                            input_path, OUTPUT_FOLDER,
                            strength, enhance_after, blur_type,
                            motion_length, motion_angle,
                            denoise_before, extra_iters, derain_before,
                        )
                        overlay_path, mask_path = compute_diff_visual(
                            input_path, output_path, OUTPUT_FOLDER
                        )

            elif action == "enhance":
                output_path = enhance_image(input_path, OUTPUT_FOLDER)

            elif action == "detect":
                output_path = detect_objects(input_path, OUTPUT_FOLDER)

            else:  # recognize
                output_path, classes = recognize_image(input_path, OUTPUT_FOLDER)

            orig_name = os.path.basename(input_path)
            out_name = os.path.basename(output_path)
            overlay_name = os.path.basename(overlay_path) if overlay_path else None
            mask_name = os.path.basename(mask_path) if mask_path else None

            resp = {
                "original": input_path,
                "output": output_path,
                "original_url": f"/uploads/{orig_name}",
                "output_url": f"/outputs/{out_name}",
                "overlay_url": (f"/outputs/{overlay_name}" if overlay_name else None),
                "mask_url": (f"/outputs/{mask_name}" if mask_name else None),
            }
            if classes is not None:
                resp["classes"] = classes
            return jsonify(resp)

        except Exception as exc:
            print(f"[api/process] ERROR action={action}: {exc}", flush=True)
            traceback.print_exc()
            return jsonify({"error": str(exc)}), 500

    # ── Text-to-image (direct path, not job-based) ───────────────────────────
    elif action == "generate_text":
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        try:
            output_path = generate_from_text(prompt, OUTPUT_FOLDER)
            out_name = os.path.basename(output_path)
            return jsonify({"output": output_path, "output_url": f"/outputs/{out_name}"})
        except Exception as exc:
            traceback.print_exc()
            return jsonify({"error": str(exc)}), 500

    # ── Img2img ──────────────────────────────────────────────────────────────
    elif action == "generate_image":
        if not file:
            return jsonify({"error": "No image provided"}), 400
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        try:
            input_path = save_file(file, UPLOAD_FOLDER)
            output_path = generate_from_image(input_path, prompt, OUTPUT_FOLDER)
            orig_name = os.path.basename(input_path)
            out_name = os.path.basename(output_path)
            return jsonify({
                "original": input_path,
                "output": output_path,
                "original_url": f"/uploads/{orig_name}",
                "output_url": f"/outputs/{out_name}",
            })
        except Exception as exc:
            traceback.print_exc()
            return jsonify({"error": str(exc)}), 500

    # ── Sketch-to-image ──────────────────────────────────────────────────────
    elif action == "sketch_to_image":
        if not file:
            return jsonify({"error": "No image provided"}), 400
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        try:
            input_path = save_file(file, UPLOAD_FOLDER)
            output_path = generate_from_sketch(input_path, prompt, OUTPUT_FOLDER)
            orig_name = os.path.basename(input_path)
            out_name = os.path.basename(output_path)
            return jsonify({
                "original": input_path,
                "output": output_path,
                "original_url": f"/uploads/{orig_name}",
                "output_url": f"/outputs/{out_name}",
            })
        except RuntimeError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as exc:
            traceback.print_exc()
            return jsonify({"error": str(exc)}), 500

    else:
        return jsonify({"error": "Unknown action"}), 400


@app.route("/api/vault")
def api_vault():
    outputs = []
    if os.path.exists(OUTPUT_FOLDER):
        files = [
            f for f in os.listdir(OUTPUT_FOLDER)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]
        files.sort(
            key=lambda x: os.path.getmtime(os.path.join(OUTPUT_FOLDER, x)),
            reverse=True,
        )
        for f in files:
            outputs.append({
                "name": f,
                "url": f"/outputs/{f}",
                "timestamp": os.path.getmtime(os.path.join(OUTPUT_FOLDER, f)),
            })
    return jsonify(outputs)


@app.route("/uploads/<path:filename>")
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/outputs/<path:filename>")
def serve_outputs(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
