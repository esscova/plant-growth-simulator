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
def normalizar(luz: float, agua: float) -> tuple:
    luz_norm = (luz - 0) / (12 - 0) * 2 - 1  # 0 a 12 -> -1 a 1
    agua_norm = (agua - 0) / (100 - 0) * 2 - 1  # 0 a 100 -> -1 a 1
    return luz_norm, agua_norm

def prever(luz: float, agua: float) -> float:
    luz_norm, agua_norm = normalizar(luz, agua)
    x = np.array([[1, luz_norm, agua_norm, luz_norm * agua_norm]])
    return modelo.predict(x)[0]

def gerar_dados_grafico(luz_atual: float, agua_atual: float) -> dict:
    # dados para plot
    luz_vals = np.linspace(0, 12, 20)  # 20 pontos de 0 a 12 horas
    agua_vals = np.linspace(0, 100, 20)  # 20 pontos de 0 a 100 ml

    # Curva 1: Altura vs Luz, com Água fixa no valor atual
    alturas_luz = [prever(l, agua_atual) for l in luz_vals]

    # Curva 2: Altura vs Água, com Luz fixa no valor atual
    alturas_agua = [prever(luz_atual, a) for a in agua_vals]

    # Ponto atual do usuário
    altura_atual = prever(luz_atual, agua_atual)

    return {
        'luz_vals': luz_vals.tolist(),
        'agua_vals': agua_vals.tolist(),
        'alturas_luz': alturas_luz,
        'alturas_agua': alturas_agua,
        'luz_atual': luz_atual,
        'agua_atual': agua_atual,
        'altura_atual': altura_atual
    }

# rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    luz = float(request.form['luz'])
    agua = float(request.form['agua'])
    dados_grafico = gerar_dados_grafico(luz, agua)
    return jsonify({
        'altura': round(dados_grafico['altura_atual'], 2),
        'grafico': dados_grafico
    })

if __name__ == '__main__':
    app.run(debug=True)