from flask import Flask, render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/registro')
def register():
    return render_template('Registrarse.html')

if __name__ == "__main__":
    app.run()


