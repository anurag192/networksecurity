
# 🔐 Network Security Threat Detection - End-to-End ML Pipeline

This is an end-to-end machine learning project to detect potential network security threats using various traffic-related features. The system is designed to automate the full ML pipeline from data ingestion, preprocessing, model training, evaluation, versioning, and deployment via a web interface.

---

## 🚀 Tech Stack

- **Python**: Core programming language.
- **pandas, NumPy**: Data preprocessing and manipulation.
- **scikit-learn**: Model training and evaluation.
- **MongoDB**: Used as a NoSQL database for storing and retrieving network data.
- **Flask**: For deploying the model as an API.
- **Docker**: Containerized deployment of the app.
- **DVC**: For data and model version control (optional).
- **HTML + Jinja**: Web template rendering.
- **MLflow** *(optional)*: For tracking experiments.
- **Logging**: Logging infrastructure for pipeline monitoring.

---

## 📁 Project Structure

```
.
├── Network_Data/           # MongoDB data setup and raw files
├── data_schema/            # Transformed or structured data
├── final_models/           # Trained models and artifacts
├── logs/                   # Training and deployment logs
├── networksecurity/        # Core logic for security detection
├── prediction/             # Inference-related code
├── templates/              # Flask HTML templates
├── valid_data/             # Validated datasets
├── app.py                  # Flask deployment script
├── main.py                 # Model training and evaluation
├── push_data.py            # MongoDB data insertion
├── test_mongodb.py         # MongoDB connection test
├── requirements.txt        # Python dependencies
├── setup.py                # Setup configuration
├── Dockerfile              # Docker container configuration
├── README.md               # Project documentation (this file)
└── .gitignore              # Git ignore rules
```

---

## 🧠 Features

- Automated ingestion of raw data into MongoDB.
- Schema validation and transformation.
- Model training using multiple ML algorithms (e.g., Random Forest, SVM).
- Trained model artifacts stored and versioned.
- Flask-based API for prediction from user inputs.
- Clean and interactive frontend for live threat prediction.
- Docker support for easy deployment and portability.
- Logs and metrics tracking.

---

## 🛠️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/network-security-ml-project.git
   cd network-security-ml-project
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **MongoDB Setup**
   - Start your MongoDB server locally or via cloud (e.g., MongoDB Atlas).
   - Run the following to push data:
     ```bash
     python push_data.py
     ```

4. **Train the Model**
   ```bash
   python main.py
   ```

5. **Test MongoDB Connection**
   ```bash
   python test_mongodb.py
   ```

6. **Run the Web Application**
   ```bash
   python app.py
   ```


   ```

---

## ⚙️ Automation Workflow (CI/CD-ready)

The entire workflow can be automated using:
- **Shell scripts or Makefile** for orchestration.
- **DVC pipelines** for reproducibility.
- **GitHub Actions  for CI/CD.

---

## 📊 Output

- Trained models with high accuracy in threat classification.
- Live prediction via web UI.


---


