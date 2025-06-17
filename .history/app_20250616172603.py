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

@app.route('/train', methods=['POST'])
def train():
    try:
        model_score = train_pipeline()
        return jsonify({
            'success': True,
            'score': model_score
        })
    except Exception as e:
        logger.error(f"Error in training: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data_path = os.path.join('artifacts', 'transformed_data.csv')
        model_path = os.path.join('artifacts', 'model.pkl')
        
        predictions = predict_new_data(model_path, data_path)
        results_path = os.path.join('artifacts', 'predictions.csv')
        results_df = pd.read_csv(results_path)
        
        results = results_df.tail(30).to_dict('records')
        return jsonify({
            'success': True,
            'predictions': results
        })
        
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)