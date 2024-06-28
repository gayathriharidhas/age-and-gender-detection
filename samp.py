import torch
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image

# Load pre-trained models and feature extractors
gender_model_name = "rizvandwiki/gender-classification"
age_model_name = "cledoux42/Age_Classify_v001"

gender_feature_extractor = AutoFeatureExtractor.from_pretrained(gender_model_name)
gender_model = AutoModelForImageClassification.from_pretrained(gender_model_name)

age_feature_extractor = AutoFeatureExtractor.from_pretrained(age_model_name)
age_model = AutoModelForImageClassification.from_pretrained(age_model_name)

# Function to classify gender from image
def classify_gender(image):
    inputs = gender_feature_extractor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = gender_model(**inputs)

    predictions = torch.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(predictions, dim=-1).item()

    labels = gender_model.config.id2label
    predicted_label = labels[predicted_class]

    return predicted_label

# Function to classify age from image
def classify_age(image):
    inputs = age_feature_extractor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = age_model(**inputs)

    predictions = torch.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(predictions, dim=-1).item()

    labels = age_model.config.id2label
    predicted_label = labels[predicted_class]

    return predicted_label

# Function to classify both age and gender from image
def classify_age_and_gender(image_path):
    image = Image.open(image_path).convert("RGB")
    
    print("///////////ronald")

    predicted_gender = classify_gender(image)
    predicted_age = classify_age(image)

    return predicted_age, predicted_gender

# Example usage
# image_path = r"C:\Users\LENOVO\Desktop\age&gender\static\img6.jpg"
# predicted_age, predicted_gender = classify_age_and_gender(image_path)
# print(f"Predicted age: {predicted_age}")
# print(f"Predicted gender: {predicted_gender}")
# import face_recognition

# def are_faces_same(image_path1, image_path2):
#     # Load the images
#     image1 = face_recognition.load_image_file(image_path1)
#     image2 = face_recognition.load_image_file(image_path2)

#     # Find face encodings in both images
#     face_encoding1 = face_recognition.face_encodings(image1)
#     face_encoding2 = face_recognition.face_encodings(image2)

#     # Check if any faces were found in both images
#     if len(face_encoding1) == 0 or len(face_encoding2) == 0:
#         print("No faces found in one or both images.")
#         return False

#     # Compare the face encodings
#     result = face_recognition.compare_faces([face_encoding1[0]], face_encoding2[0])

#     # Print the result
#     if resul…