from flask import Flask, request, jsonify
import pandas as pd
import random
from PIL import Image
import io
import numpy as np
from sklearn.cluster import KMeans
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
import torch.nn as nn

app = Flask(__name__)

# Load dataset
try:
    df = pd.read_csv('shirts_only.csv')
    images_df = pd.read_csv('images.csv')
    # Strip .jpg from filename to match id
    images_df['filename'] = images_df['filename'].str.replace('.jpg', '').astype(int)
    images_df.rename(columns={'filename': 'id'}, inplace=True)
    # Merge untuk link gambar
    df = df.merge(images_df, on='id', how='left')
except Exception as e:
    df = pd.DataFrame()
    print(f"Error loading data: {e}")

# Load pre-trained ResNet50 for feature extraction
model = resnet50(pretrained=True)
model.eval()
# Remove the last layer
model = nn.Sequential(*list(model.children())[:-1])

# Transform for input images
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_features(image):
    """Extract features from image using ResNet50"""
    img_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        features = model(img_tensor)
    return features.squeeze().numpy()

def get_dominant_color(image):
    """Get dominant color from image"""
    image = image.resize((150, 150))
    img_array = np.array(image)
    img_array = img_array.reshape((img_array.shape[0] * img_array.shape[1], 3))
    
    kmeans = KMeans(n_clusters=1, n_init=10)
    kmeans.fit(img_array)
    dominant_color = kmeans.cluster_centers_[0]
    
    # Convert to color name (simple mapping)
    colors = {
        'Red': [255, 0, 0],
        'Green': [0, 255, 0],
        'Blue': [0, 0, 255],
        'White': [255, 255, 255],
        'Black': [0, 0, 0],
        'Yellow': [255, 255, 0],
        'Purple': [128, 0, 128],
        'Pink': [255, 192, 203],
        'Brown': [165, 42, 42],
        'Grey': [128, 128, 128],
        'Navy Blue': [0, 0, 128],
        'Orange': [255, 165, 0]
    }
    
    min_dist = float('inf')
    color_name = 'Unknown'
    for name, rgb in colors.items():
        dist = np.linalg.norm(dominant_color - np.array(rgb))
        if dist < min_dist:
            min_dist = dist
            color_name = name
    
    return color_name

@app.route('/')
def home():
    return "API Scanner Aktif."

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image'}), 400
    
    file = request.files['image']
    image = Image.open(io.BytesIO(file.read()))
    
    # Extract dominant color
    dominant_color = get_dominant_color(image)
    
    # Filter recommendations based on color
    if not df.empty:
        color_matches = df[df['baseColour'].str.lower() == dominant_color.lower()]
        if len(color_matches) >= 6:
            recommendations = color_matches.sample(n=6).to_dict(orient='records')
        else:
            # If not enough, add random
            remaining = 6 - len(color_matches)
            random_recs = df.sample(n=min(remaining, len(df))).to_dict(orient='records')
            recommendations = color_matches.to_dict(orient='records') + random_recs
    else:
        recommendations = []

    return jsonify({
        'status': 'success',
        'dominant_color': dominant_color,
        'recommendations': recommendations
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
