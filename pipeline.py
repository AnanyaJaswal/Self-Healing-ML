import logging
import sys
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Set up logging (Monitoring & Feedback Loop)
logging.basicConfig(filename='pipeline_health.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_ml_pipeline():
    logging.info("Starting ML Pipeline...")
    
    try:
        # 1. Data Ingestion
        logging.info("Loading Data...")
        data = load_iris()
        X, y = data.data, data.target
        
        # SIMULATE A DATA DRIFT / CORRUPTION ANOMALY
        # We read a toggle from a file. If 'corrupt', we mess up the data.
        with open("status.txt", "r") as f:
            status = f.read().strip()
            
        if status == "corrupt":
            logging.warning("Data anomaly detected during ingestion!")
            # Introduce massive data corruption so the model learns nothing
            X = [[0, 0, 0, 0]] * len(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 2. Model Training
        logging.info("Training Model...")
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        # 3. Monitoring & Validation
        logging.info("Validating Model...")
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        logging.info(f"Model Accuracy: {accuracy:.2f}")

        # Anomaly Detection Trigger
        if accuracy < 0.80:
            logging.error(f"Accuracy {accuracy:.2f} is below threshold. Halting.")
            print(f"FAILED: Accuracy {accuracy:.2f} too low.")
            sys.exit(1) # Crash the script

        logging.info("Pipeline completed successfully. Model deployed.")
        print("SUCCESS: Model trained and healthy!")

    except Exception as e:
        logging.error(f"System Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_ml_pipeline()
