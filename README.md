# FastAPI Project

## 📄 Assignment
The details of the assignment are provided in the following document:  
[Assignment](assignment.pdf)

---
## 🚀 Project Setup

This project is developed with **FastAPI**.  
Follow the steps below to set up the environment and run the application.

### 1. Install dependencies

If you're on mac
```bash
brew install uv
```

If you're on win
```bash
pip install uv
```

Install dependencies
```bash
uv pip compile requirements.in -o requirements.txt
uv pip install -r requirements.txt
```

### 2. Run the application
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Test the application importing the postman collection
[Postman Collection](Artificialy.postman_collection.json)

