from flask import Flask, request, jsonify, render_template
from datetime import datetime
from surge_pricing import calculate_surge_multiplier

app = Flask(__name__)


@app.route('/')
def index():
    # Render the simple web interface
    return render_template('index.html')


@app.route('/calculate_fare', methods=['POST'])
def calculate_fare():
    # Check if request is JSON or form data and extract parameters accordingly
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    try:
        base_fare = float(data.get('base_fare', 10.0))
        demand = float(data.get('demand', 1))
        supply = float(data.get('supply', 1))
        # Accept event as a string from form or boolean from JSON; convert accordingly
        event = data.get('event', 'false')
        if isinstance(event, str):
            event = event.lower() == 'true'
    except ValueError:
        return jsonify({'error': 'Invalid input values'}), 400

    surge_multiplier = calculate_surge_multiplier(demand, supply, datetime.now(), event)
    final_fare = round(base_fare * surge_multiplier, 2)
    result = {
        'base_fare': base_fare,
        'surge_multiplier': surge_multiplier,
        'final_fare': final_fare
    }

    # Return JSON if API call, or render result on the web page
    if request.is_json:
        return jsonify(result)
    else:
        return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
