from flask import Flask, request, render_template_string, jsonify
from calculator import Calculator

app = Flask(__name__)
calc = Calculator()

# HTML/CSS/JavaScript for the calculator
CALCULATOR_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Arial', sans-serif;
        }
        
        .calculator {
            background: #1a1a2e;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            width: 320px;
        }
        
        .display {
            background: #16213e;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: right;
            min-height: 80px;
        }
        
        .display .expression {
            color: #8892b0;
            font-size: 16px;
            min-height: 24px;
            word-wrap: break-word;
        }
        
        .display .result {
            color: #ffffff;
            font-size: 36px;
            font-weight: bold;
            min-height: 44px;
            transition: all 0.3s;
        }
        
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }
        
        button {
            padding: 20px;
            font-size: 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s;
            background: #2a2a4a;
            color: white;
            font-weight: bold;
        }
        
        button:hover {
            transform: scale(1.05);
            filter: brightness(1.2);
        }
        
        button:active {
            transform: scale(0.95);
        }
        
        .btn-number {
            background: #2a2a4a;
        }
        
        .btn-number:hover {
            background: #3a3a5a;
        }
        
        .btn-operator {
            background: #4a4a8a;
        }
        
        .btn-operator:hover {
            background: #5a5a9a;
        }
        
        .btn-equals {
            background: #667eea;
            grid-column: span 1;
        }
        
        .btn-equals:hover {
            background: #7a8efc;
        }
        
        .btn-clear {
            background: #e74c3c;
        }
        
        .btn-clear:hover {
            background: #ff6b5b;
        }
        
        .btn-zero {
            grid-column: span 2;
        }
        
        .btn-function {
            background: #2d2d4a;
        }
        
        .btn-function:hover {
            background: #3d3d5a;
        }
        
        .error {
            color: #e74c3c !important;
        }
        
        @media (max-width: 400px) {
            .calculator {
                width: 280px;
                padding: 20px;
            }
            
            button {
                padding: 15px;
                font-size: 18px;
            }
        }
    </style>
</head>
<body>
    <div class="calculator">
        <div class="display">
            <div class="expression" id="expression"></div>
            <div class="result" id="result">0</div>
        </div>
        <div class="buttons">
            <button class="btn-clear" onclick="clearAll()">AC</button>
            <button class="btn-function" onclick="toggleSign()">±</button>
            <button class="btn-function" onclick="percentage()">%</button>
            <button class="btn-operator" onclick="appendOperator('/')">÷</button>
            
            <button class="btn-number" onclick="appendNumber('7')">7</button>
            <button class="btn-number" onclick="appendNumber('8')">8</button>
            <button class="btn-number" onclick="appendNumber('9')">9</button>
            <button class="btn-operator" onclick="appendOperator('*')">×</button>
            
            <button class="btn-number" onclick="appendNumber('4')">4</button>
            <button class="btn-number" onclick="appendNumber('5')">5</button>
            <button class="btn-number" onclick="appendNumber('6')">6</button>
            <button class="btn-operator" onclick="appendOperator('-')">−</button>
            
            <button class="btn-number" onclick="appendNumber('1')">1</button>
            <button class="btn-number" onclick="appendNumber('2')">2</button>
            <button class="btn-number" onclick="appendNumber('3')">3</button>
            <button class="btn-operator" onclick="appendOperator('+')">+</button>
            
            <button class="btn-number btn-zero" onclick="appendNumber('0')">0</button>
            <button class="btn-number" onclick="appendDecimal()">.</button>
            <button class="btn-equals" onclick="calculate()">=</button>
        </div>
    </div>

    <script>
        let currentInput = '0';
        let previousInput = '';
        let operation = null;
        let shouldResetScreen = false;
        let expression = '';

        function updateDisplay() {
            const resultElement = document.getElementById('result');
            const expressionElement = document.getElementById('expression');
            
            // Format the current input with commas for readability
            let displayValue = currentInput;
            if (displayValue !== 'Error' && !displayValue.includes('.')) {
                // Don't format during typing to avoid cursor issues
            }
            
            resultElement.textContent = displayValue;
            expressionElement.textContent = expression;
            
            // Reset error class if present
            resultElement.classList.remove('error');
        }

        function appendNumber(number) {
            if (shouldResetScreen) {
                currentInput = '';
                shouldResetScreen = false;
            }
            
            if (number === '.' && currentInput.includes('.')) return;
            
            if (currentInput === '0' && number !== '.') {
                currentInput = number;
            } else {
                currentInput += number;
            }
            
            updateDisplay();
        }

        function appendDecimal() {
            if (shouldResetScreen) {
                currentInput = '0';
                shouldResetScreen = false;
            }
            if (!currentInput.includes('.')) {
                currentInput += '.';
            }
            updateDisplay();
        }

        function appendOperator(op) {
            const current = parseFloat(currentInput);
            if (previousInput !== '' && !shouldResetScreen) {
                calculate();
            }
            
            previousInput = currentInput;
            operation = op;
            expression = currentInput + ' ' + getSymbol(op) + ' ';
            shouldResetScreen = true;
            updateDisplay();
        }

        function getSymbol(op) {
            const symbols = {
                '+': '+',
                '-': '−',
                '*': '×',
                '/': '÷'
            };
            return symbols[op] || op;
        }

        function calculate() {
            if (operation === null || shouldResetScreen) return;
            
            const a = parseFloat(previousInput);
            const b = parseFloat(currentInput);
            
            // Show the full expression
            expression = previousInput + ' ' + getSymbol(operation) + ' ' + currentInput + ' =';
            
            // Make API call to backend
            fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    a: a,
                    b: b,
                    operation: operation
                })
            })
            .then(response => response.json())
            .then(data => {
                const resultElement = document.getElementById('result');
                if (data.error) {
                    resultElement.textContent = 'Error';
                    resultElement.classList.add('error');
                    currentInput = 'Error';
                } else {
                    let result = data.result;
                    // Format the result
                    if (Number.isInteger(result)) {
                        result = result.toString();
                    } else {
                        result = result.toFixed(8).replace(/\.?0+$/, '');
                    }
                    resultElement.textContent = result;
                    currentInput = result;
                    expression = data.expression || expression;
                }
                previousInput = '';
                operation = null;
                shouldResetScreen = true;
                document.getElementById('expression').textContent = expression;
            })
            .catch(error => {
                document.getElementById('result').textContent = 'Error';
                document.getElementById('result').classList.add('error');
                currentInput = 'Error';
            });
        }

        function clearAll() {
            currentInput = '0';
            previousInput = '';
            operation = null;
            shouldResetScreen = false;
            expression = '';
            updateDisplay();
        }

        function toggleSign() {
            if (currentInput === '0' || currentInput === 'Error') return;
            if (currentInput.startsWith('-')) {
                currentInput = currentInput.slice(1);
            } else {
                currentInput = '-' + currentInput;
            }
            updateDisplay();
        }

        function percentage() {
            const current = parseFloat(currentInput);
            if (isNaN(current)) return;
            currentInput = (current / 100).toString();
            updateDisplay();
        }

        // Keyboard support
        document.addEventListener('keydown', (e) => {
            if (e.key >= '0' && e.key <= '9') {
                appendNumber(e.key);
            } else if (e.key === '.') {
                appendDecimal();
            } else if (e.key === '+') {
                appendOperator('+');
            } else if (e.key === '-') {
                appendOperator('-');
            } else if (e.key === '*') {
                appendOperator('*');
            } else if (e.key === '/') {
                e.preventDefault();
                appendOperator('/');
            } else if (e.key === 'Enter' || e.key === '=') {
                e.preventDefault();
                calculate();
            } else if (e.key === 'Escape' || e.key === 'c') {
                clearAll();
            } else if (e.key === '%') {
                percentage();
            }
        });

        // Initialize display
        updateDisplay();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Render the calculator interface"""
    return render_template_string(CALCULATOR_HTML)

@app.route('/calculate', methods=['POST'])
def calculate():
    """Handle calculation requests from the frontend"""
    try:
        data = request.get_json()
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
        operation = data.get('operation')
        
        # Build expression for display
        op_symbols = {
            '+': '+',
            '-': '−',
            '*': '×',
            '/': '÷'
        }
        expression = f"{a} {op_symbols.get(operation, operation)} {b} ="
        
        # Perform calculation
        if operation == '+':
            result = calc.add(a, b)
        elif operation == '-':
            result = calc.subtract(a, b)
        elif operation == '*':
            result = calc.multiply(a, b)
        elif operation == '/':
            result = calc.divide(a, b)
        else:
            return jsonify({'error': 'Invalid operation'}), 400
            
        return jsonify({
            'result': result,
            'expression': expression
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
