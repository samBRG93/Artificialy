# Cleaning Robot

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

### 2. ▶️ Run the Application

Start the FastAPI server with:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 3. 🧪 Testing the Application
[Postman Collection](Artificialy.postman_collection.json)


#### 🔹 Important Notes
- Before performing operations, you must **create a map** as the first step.  
- Each map requires an **ID** that will be used as a reference in subsequent operations.  
- According to the assignment specification, the map must be **square-shaped**.  
  - Non-square maps are technically possible, but they are rejected by validation rules defined in the Pydantic model.

---

#### 📂 Example Maps
To get started quickly, you can upload one of the example maps provided:

- Text format → [Txt Map](map.txt)  
- JSON format → [Json Map](map.json)
