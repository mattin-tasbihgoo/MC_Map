from flask import Flask, request, send_from_directory, jsonify
from map import generate_minecraft_map  # Import the function

app = Flask(__name__)

# Global variable to store the latest location
latest_location = {"latitude": None, "longitude": None}

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/location", methods=["POST"])
def handle_location():
    global latest_location
    data = request.json
    lat = data['latitude']
    lng = data['longitude']
    latest_location = {"latitude": lat, "longitude": lng}
    print(f"Received location from browser: {lat}, {lng}")
    
    # Call the generate_minecraft_map function with the received coordinates
    api_key = "AIzaSyAvZo7Hs4eAo0D35lNeuIpYtPY_NU-0sSE"  # Replace with your actual API key
    output_dir = "./output"
    final_image = generate_minecraft_map(lat, lng, api_key, output_dir)
    
    if final_image:
        final_image_path = f"{output_dir}/final_map_overlay.png"
        return send_from_directory(output_dir, "final_map_overlay.png")
    else:
        return "Error generating map", 500

@app.route("/current_location", methods=["GET"])
def current_location():
    return jsonify(latest_location)

if __name__ == "__main__":
    app.run(debug=True, port=5000)