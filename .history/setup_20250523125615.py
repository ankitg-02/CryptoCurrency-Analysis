from setuptools import setup, find_packages

setup(
    name='crypto-analysis',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas==1.5.3',
        'numpy==1.24.4',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'requests',
        'flask'
    ],
)
