from flask import Flask, send_from_directory, Response, render_template, redirect, url_for, request
from flask_socketio import SocketIO, emit
from prometheus_client import Counter, generate_latest, Gauge
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
CORS(app)

CHUNK_LATENCY = Gauge('chunk_latency', 'Latency in calling chunk api call')

@app.route('/metrics', methods=['GET'])
def metrics():
    # Expose Prometheus metrics
    return Response(generate_latest(), mimetype="text/plain")


@app.route('/update_latency', methods=['POST'])
def update_latency():
    """
    Endpoint to update the CHUNK_LATENCY Gauge.
    Expects a JSON payload with a 'value' key.
    """
    try:
        # Parse the JSON payload
        data = request.json
        value = data.get('value')

        # Validate the input
        if value is None or not isinstance(value, (int, float)):
            return {"error": "Invalid or missing 'value'. Must be a number."}, 400

        # Update the CACHE_MISSES Gauge
        CHUNK_LATENCY.set(value)
        return {"message": f"Chunk latency updated to {value}"}, 200

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500


if __name__ == "__main__":
    # Run the server on port 8500
    app.run(debug=True, port=8500)
