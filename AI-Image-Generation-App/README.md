# 🧠 AI Image Generation App

A full-stack **MERN** web application that allows users to generate stunning **AI-powered images** from text prompts using the **OpenAI API**.  
Built with **MongoDB**, **Express.js**, **React.js**, and **Node.js**, this project demonstrates seamless integration between frontend creativity and backend intelligence.

---

## 🚀 Features

- 🖼️ Generate high-quality AI images from text prompts  
- 💾 Save and view generated images in a community feed  
- 📤 Share AI-generated artwork with others  
- ⚡ Real-time image rendering with OpenAI API  
- 🌐 Responsive and modern UI built with React  
- 🔒 Secure backend API with Node.js and Express  
- 🧩 MongoDB for storing posts and image data  

---

## 🛠️ Tech Stack

| Category            | Technologies                  |
|---------------------|-------------- ----------------|
| **Frontend**        | React.js, Tailwind CSS, Axios |
| **Backend**         | Node.js, Express.js           |
| **Database**        | MongoDB, Mongoose             |
| **AI Model**        | OpenAI DALL·E API             |
| **Version Control** | Git, GitHub                   |

---

## 📂 Folder Structure
AI-Image-Generation-App/
│
├── client/ # React frontend
│ ├── src/
│ │ ├── components/ # Reusable UI components
│ │ ├── pages/ # Home, CreatePost, etc.
│ │ └── utils/ # Helper functions
│ └── package.json
│
├── server/ # Node.js + Express backend
│ ├── routes/ # API routes
│ ├── controllers/ # Logic for OpenAI and posts
│ ├── models/ # MongoDB schema
│ └── package.json
│
├── .env # API keys and environment variables
├── README.md
└── package.json


---

## ⚙️ Installation & Setup

1️⃣ Clone the Repository
git clone https://github.com/anurag-dhondge/Projects/AI-Image-Generation-App.git
cd AI-Image-Generation-App

2️⃣ Install Dependencies
Backend
cd server
npm install

Frontend
cd ../client
npm install

3️⃣ Set Environment Variables

Create a .env file inside the server folder and add:

OPENAI_API_KEY=your_openai_api_key
MONGODB_URL=your_mongodb_connection_string
PORT=8080

4️⃣ Run the App
Backend
cd server
npm start

Frontend
cd client
npm run dev


Visit: http://localhost:5173
 (or your configured port)

💡 Example Usage

Enter a text prompt like

“A futuristic city skyline at sunset in cyberpunk style”

Click Generate to let AI create your image.

Download, save, or share your generated art!

🧩 Future Enhancements

🗂️ Add user authentication and personalized galleries

📱 Mobile app version with React Native

🎨 Add style filters and variation options

🌍 Deploy on cloud (Render / Vercel / Netlify + MongoDB Atlas)

🧑‍💻 Author

Anurag Dhondge
🎓 B.E. Artificial Intelligence & Machine Learning
