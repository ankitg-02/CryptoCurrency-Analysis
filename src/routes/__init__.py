from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
import pandas as pd
import numpy as np
from src.models.user import db, User
from src.pipeline.predict_pipeline import predict_new_data
from src.pipeline.train_pipeline import train_pipeline
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('main.register'))
            
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful!')
        return redirect(url_for('main.login'))
        
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            user.last_login = datetime.now()
            db.session.commit()
            return redirect(url_for('main.dashboard'))
            
        flash('Invalid username or password')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        current_user.predictions += 1
        db.session.commit()
        
        data_path = 'artifacts/transformed_data.csv'
        model_path = 'artifacts/model.pkl'
        
        predictions = predict_new_data(model_path, data_path)
        original_data = pd.read_csv(data_path)
        
        # Calculate volatility
        returns = original_data['close'].pct_change()
        volatility = returns.rolling(window=20).std()
        
        results_df = pd.DataFrame({
            'time': original_data['time'],
            'actual_close': original_data['close'],
            'predicted_close': predictions,
            'volatility': volatility
        }).tail(30)
        
        return jsonify({
            'success': True,
            'predictions': results_df.to_dict('records')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/train', methods=['POST'])
@login_required
def train():
    try:
        model_score = train_pipeline()
        return jsonify({
            'success': True,
            'score': float(model_score)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500