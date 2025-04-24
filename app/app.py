from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from io import BytesIO

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")

# Load the trained model
model = load_model("C:\\Users\\HP\\Desktop\\Image_Classification_Devops\\saved_model\\image_classification_model.h5")

# Define your class names (update these as per your trained model)
class_names = ['airplane', 'car', 'cat', 'dog', 'flower', 'fruit', 'motorbike', 'person']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in request'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    try:
        # Read image as BytesIO
        img_bytes = BytesIO(file.read())

        # Load and preprocess the image
        img = image.load_img(img_bytes, target_size=(150, 150))  # Ensure the input size matches your model
        img_array = image.img_to_array(img) / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions)]
        confidence = float(np.max(predictions))

        return jsonify({
            'class': predicted_class,
            'confidence': round(confidence * 100, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
