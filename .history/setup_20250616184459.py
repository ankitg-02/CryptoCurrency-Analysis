from setuptools import setup, find_packages

setup(
    name="crypto_analysis",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-login',
        'flask-sqlalchemy',
        'flask-bcrypt',
        'python-dotenv',
        'pandas',
        'numpy',
        'scikit-learn',
        'catboost',
        'requests'
    ]
)
