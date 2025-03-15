let chart;

function simular() {
    const luz = document.getElementById('luz').value;
    const agua = document.getElementById('agua').value;
    
    // indicador de carregamento
    document.getElementById('resultado').innerHTML = '<span>Calculando...</span>';
    
    fetch('/predict', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `luz=${luz}&agua=${agua}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('resultado').innerHTML = `Altura prevista: <span>${data.altura} cm</span>`;
        atualizarGrafico(data.grafico);
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('resultado').innerHTML = 'Erro na simulação. Tente novamente.';
    });
}

function atualizarGrafico(dados) {
    const ctx = document.getElementById('grafico').getContext('2d');
    
    if (chart) {
        chart.destroy(); // existe grafico? 
    }

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: `Altura vs Luz (Água = ${dados.agua_atual} ml)`,
                    data: dados.luz_vals.map((luz, i) => ({x: luz, y: dados.alturas_luz[i]})),
                    borderColor: '#4CAF50',
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                },
                {
                    label: `Altura vs Água (Luz = ${dados.luz_atual} horas)`,
                    data: dados.agua_vals.map((agua, i) => ({x: agua, y: dados.alturas_agua[i]})),
                    borderColor: '#2196F3',
                    backgroundColor: 'rgba(33, 150, 243, 0.1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                },
                {
                    label: 'Configuração Atual',
                    data: [{x: dados.luz_atual, y: dados.altura_atual}],
                    borderColor: '#FF5722',
                    backgroundColor: '#FF5722',
                    pointRadius: 8,
                    pointHoverRadius: 10,
                    showLine: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Luz (horas) ou Água (ml)',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Altura da Planta (cm)',
                        font: {
                            weight: 'bold'
                        }
                    },
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    titleColor: '#212121',
                    bodyColor: '#212121',
                    borderColor: '#e0e0e0',
                    borderWidth: 1,
                    padding: 10,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label.split('(')[0]}: ${context.parsed.y.toFixed(2)} cm`;
                        }
                    }
                }
            }
        }
    });
}


window.onload = function() {
    simular();
}
