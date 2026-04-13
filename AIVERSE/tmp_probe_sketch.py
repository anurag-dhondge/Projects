import json
import time
import os
import sys
import subprocess

import requests

BASE = "http://127.0.0.1:3000"
IMG = "/Users/ekansh/Downloads/KTPL/Images_processing/static/uploads/ChatGPT_Image_Jan_31_2026_10_21_40_AM.png"

def main():
    r = requests.post(
        f"{BASE}/api/job/start",
        files={"image": open(IMG, "rb")},
        data={
            "action": "sketch_to_image",
            "prompt": "a detailed colored illustration",
            "steps": "5",
            "width": "256",
            "height": "256",
        },
        timeout=30,
    )
    r.raise_for_status()
    job_id = r.json()["job_id"]
    print("job_id", job_id)

    while True:
        st = requests.get(f"{BASE}/api/job/{job_id}", timeout=10)
        st.raise_for_status()
        data = st.json()
        print("status", data.get("status"), "step", data.get("step"), "/", data.get("total"), "eta", data.get("eta_s"))
        if data.get("status") in ("done", "error"):
            print(json.dumps(data, indent=2)[:2000])
            if data.get("status") == "done" and data.get("output_url"):
                out_url = f"{BASE}{data['output_url']}"
                out_path = "/tmp/visionai_probe_sketch.png"
                resp = requests.get(out_url, timeout=30)
                resp.raise_for_status()
                with open(out_path, "wb") as f:
                    f.write(resp.content)
                print("saved", out_path, "bytes", os.path.getsize(out_path))
                try:
                    from PIL import Image
                    import numpy as np

                    img = Image.open(out_path).convert("RGB")
                    a = np.array(img)
                    print("img_size", img.size)
                    print("min", int(a.min()), "max", int(a.max()), "mean", float(a.mean()))
                except Exception as e:
                    print("img_stats_failed", e)
            return
        time.sleep(0.5)


if __name__ == "__main__":
    main()
