from flask import Flask, request, jsonify
from calculator import Calculator

app = Flask(__name__)
calc = Calculator()

@app.route('/add')
def add():
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 0))
    return jsonify({'result': calc.add(a, b)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
