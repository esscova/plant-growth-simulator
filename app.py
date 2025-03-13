# coding utf-8
# python 3.12.4
# author wellington m santos - github.com/esscova
# project predicting the height of a plant

from flask import Flask, render_template, request, jsonify
import numpy as np
import statsmodels.api as sm

app = Flask(__name__)

# dados do experimento
luz = np.array([-1, 1, -1, 1, 0, 0, 0, 0])
agua = np.array([-1, -1, 1, 1, 0, 0, 0, 0])
X = np.column_stack((luz, agua, luz * agua))  
X = sm.add_constant(X)  # intercepto
y = np.array([2.5594, 5.9785, 4.9722, 9.7602, 5.5960, 4.9838, 5.6630, 5.2806])  # altura da planta
modelo = sm.OLS(y, X).fit()

# utils
def normalizar(luz: float, agua:float) -> tuple:
    """
    Função para normalizar os valores reais para escala -1 a 1

    Args:
        luz (float): luz
        agua (float): agua

    Returns:
        tuple: luz_norm, agua_norm
    """
    luz_norm = (luz - 0) / (12 - 0) * 2 - 1  # 0 a 12 -> -1 a 1
    agua_norm = (agua - 0) / (100 - 0) * 2 - 1  # 0 a 100 -> -1 a 1
    return luz_norm, agua_norm


def prever(luz: float, agua: float) -> float:
    """
    Função para prever a altura da planta

    Args:
        luz (float): luz
        agua (float): agua

    Returns:
        float: altura da planta
    """
    luz_norm, agua_norm = normalizar(luz, agua)
    x = np.array([1, luz_norm, agua_norm, luz_norm * agua_norm])
    return modelo.predict(x)[0]

# rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    luz = request.form['luz']
    agua = request.form['agua']
    altura = prever(float(luz), float(agua))
    return jsonify({'altura': altura})

if __name__ == '__main__':
    app.run(debug=True)