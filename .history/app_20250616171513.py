from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from src.pipeline.predict_pipeline import predict_new_data
from src.pipeline.train_pipeline import train_pipeline
from src.logger import logger

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from form
        data_path = os.path.join('artifacts', 'transformed_data.csv')
        model_path = os.path.join('artifacts', 'model.pkl')
        
        # Make prediction
        predictions = predict_new_data(model_path, data_path)
        
        # Load results
        results_path = os.path.join('artifacts', 'predictions.csv')
        results_df = pd.read_csv(results_path)
        
        # Convert to JSON for display
        results = results_df.tail(10).to_dict('records')
        return render_template('prediction.html', predictions=results)
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)