from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from core.map_processor import process_instruction

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

instructions_and_answers = []

@app.route('/mapa/<path:filename>')
def serve_map(filename):
    return send_from_directory('mapa', filename)

@app.route('/api/instructions', methods=['GET'])
def get_instructions():
    return jsonify(instructions_and_answers)

@app.route('/api/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        if not data or 'instruction' not in data:
            return jsonify({'error': 'Missing instruction in request'}), 400
        
        instruction = data['instruction']
        result = process_instruction(instruction)
        instructions_and_answers.append({'instruction': instruction, 'answer': result})
        return jsonify({'description': result.strip('<>')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/instructions', methods=['GET'])
def display_instructions():
    return render_template('instructions.html', instructions=instructions_and_answers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 