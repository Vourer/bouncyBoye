from flask import Flask, render_template, request, url_for
import program as pro

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/wynik')
def wynik():
    return render_template('wynik.html')

@app.route('/dane', methods=['GET', 'POST'])
def dane():
    v0 = int(request.form.get('v0',''))
    h0 = int(request.form.get('h0',''))
    m = float(request.form.get('m',''))
    gamma = float(request.form.get('gamma',''))
    tmax = int(request.form.get('tmax',''))
    dt = float(request.form.get('dt',''))
    czas, odbicia, hmax = pro.przygotuj_symulacje(v0, h0, m, gamma, tmax, dt)
    return render_template('wynik.html', czas=round(czas,2), odbicia=odbicia, hmax=round(hmax,2))


if __name__ == "__main__":
    app.run()