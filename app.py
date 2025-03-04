from flask import Flask, render_template, request, redirect, url_for
from waitress import serve

app = Flask(__name__)

# Lista para armazenar os lançamentos
launches = []

@app.route('/')
def index():
    return render_template('index.html', launches=launches)

@app.route('/add', methods=['POST'])
def add_launch():
    truck = request.form['truck']
    driver = request.form['driver']
    load_date = request.form['load_date']
    unload_date = request.form['unload_date']
    load_location = request.form['load_location']
    unload_location = request.form['unload_location']
    expense = request.form['expense']
    revenue = request.form['revenue']

    # Adiciona o lançamento à lista
    launches.append({
        'truck': truck,
        'driver': driver,
        'load_date': load_date,
        'unload_date': unload_date,
        'load_location': load_location,
        'unload_location': unload_location,
        'expense': expense,
        'revenue': revenue,
    })

    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Servidor rodando em http://0.0.0.0:5000")
    serve(app, host="0.0.0.0", port=5000)