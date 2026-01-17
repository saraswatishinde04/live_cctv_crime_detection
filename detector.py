# detector.py
import random
import torch
import torchvision.transforms as transforms
from PIL import Image
import cv2

# Dummy placeholder for testing (later replace with actual model)
# To simulate crime detection for testing without a real model
def predict_frame(frame):
    # Simulate 1 in 50 frames as a "crime detected"
    return random.randint(0, 49) == 0

# When you have a model later, replace with this:
"""
model = torch.load('models/crime_model.pt', map_location='cpu')
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict_frame(frame):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = model(img)
    prob = torch.sigmoid(output)
    return prob.item() > 0.5
"""
