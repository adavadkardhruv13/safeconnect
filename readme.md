# 🚨 Safeconnekt

**Safeconnekt** is a mobile-first emergency response system that uses QR technology to simplify identification, improve safety, and accelerate recovery during emergencies. From tagging medical info to identifying lost pets or individuals, Safeconnekt helps bridge the critical gap between emergency and response — all with a scan.

---

## 🔐 Key Features

- 📱 **Smart QR Codes**  
  Each user, item, or pet gets a unique QR code for fast identification.

- 🆘 **Emergency-First Design**  
  Instantly access vital medical or contact details when it matters most.

- 🏷️ **Universal Tagging**  
  Attach QR tags to personal items, bags, pets, or individuals.

- ♻️ **Recovery & Reunification**  
  Drastically improve response time and recovery success.

- 🔐 **OTP-Based Authentication**  
  Secure user onboarding with one-time passwords via mobile.

- ⚙️ **Robust Backend (Django + Gunicorn)**  
  Scalable, production-ready server environment.

- 🎯 **Modern Frontend (Flutter)**  
  Smooth, cross-platform user experience.

---

## Installation


### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/adavadkardhruv13/safeconnect.git
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


4. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```
---

## 🧰 Tech Stack
### Backend
⚡ FastAPI

🛢 PostgreSQL

🌫 Cloudinary (for media storage)

☁️ AWS RDS (Relational Database Service)

### Frontend
💙 Flutter

---
