from flask import Flask, request, jsonify, json

app = Flask(__name__)

# Default data
default = {
    "Players": {
    }
}
print(default)

# Store the latest received data
latest_data = None


# Endpoint to receive JSON data
@app.route('/receive', methods=['POST'])
def receive_data():
    global latest_data
    data = request.json  # Access JSON data
    if data:
        print(data)
        if "Update" in data:
            data = data["Update"]
            default["Players"][data["id"]] = {"pos": data["pos"]}
            latest_data = default  # Update global variable
            return jsonify({"message": "Data received successfully!"}), 200
        elif "deletePetition" in data:
            data = data["deletePetition"]
            del default["Players"][data]
            latest_data = default  # Update global variable
            return jsonify({"message": "Player deleted from server!"}), 200
    return jsonify({"error": "No JSON data received"}), 400


# Endpoint to send predefined data
@app.route('/send-data', methods=['GET'])
def send_data():
    global latest_data
    # Check if there's new data to send
    if latest_data:
        return jsonify(latest_data), 200
    # Return default data if no new data has been received
    return jsonify(default), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
