from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/rfid-data', methods=['POST'])
def receive_data():
    data = request.json
    save_to_file(data)
    return "Data received", 200

def save_to_file(data):
    with open('rfid_data.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
