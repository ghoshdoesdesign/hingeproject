from flask import Flask, request, jsonify, render_template
import base64
import os
import requests

app = Flask(__name__)

# Function to encode an image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for analyzing images
@app.route('/analyze-images', methods=['POST'])
def analyze_images():
    image_files = request.files.getlist('images')
    image_paths = []

    # Save and encode images
    for image in image_files:
        image_path = os.path.join('uploads', image.filename)
        image.save(image_path)
        image_paths.append(image_path)

    # Call your existing function here to analyze the images
    result = analyze_images_with_gpt4(image_paths)

    return jsonify(result)

# Function to analyze multiple base64-encoded images with GPT-4
def analyze_images_with_gpt4(image_paths):
    api_key = os.getenv('OPENAI_API_KEY') 
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # content = [
    #     {"type": "text", "text": "You are a profile optimization assistant. Be a bit cocky in your review. Analyze the Hinge profile in the images for the following: 1. Evaluate the quality of the photos (e.g., clarity, lighting, appropriateness for dating apps). 2. Give a rating from 1 to 10 based on the overall profile quality."}
    # ]

    # content = [
    #     {"type": "text", "text": "You are a Hinge profile optimization assistant. Be a bit cocky in your review. Analyze the Hinge profile in the images for the following: 1. Evaluate the quality of the images and prompts individually (e.g., attractiveness, genuineness, motive). 2. Be very detailed in your analysis. If it is a guy’s profile, look at from a female perspective and suggest changes that would attract the opposite sex and vice versa but don't be very explicit about it. You can add a funny tinge to your analysis as well. 3. Give them a ‘Hingle appeal’ rating from 1 to 10 based on the overall profile quality. 4. Lastly put top 3 actionable things they can change about their hinge profile to make it better instantly. In your output dont put the ‘###’ in the final output. 'Lets see how I can get your more matches'- use this phrase at the beginning of your output."}
    # ]

    content = [
        {"type": "text", "text": "You are a Hinge profile optimization assistant. Analyze the Hinge profile in the images for the following: 1. Evaluate the quality of the images (Image Quality)and prompts (Prompt Quality) individually on how attractive, genuine it is. 2. If it is a guy’s profile, look at from a female perspective and suggest changes that would attract the opposite sex and vice versa but don't be very explicit about it. You can add a funny tinge to your analysis as well. 3. Give them a ‘Hinge Appeal Rating' from 1 to 10 based on the overall profile quality. 4. Lastly put 'Top 3 actionable things' they can change about their hinge profile to make it better instantly. In your output dont put the ‘###’ in the final output. 'Lets see how I can get your more matches'- use this phrase at the beginning of your output. Never mention explicitly 'the female or male perspective' but do keep it in mind. Keep your outputs to 200 words"}
    ]

    for image_path in image_paths:
        base64_image = encode_image(image_path)
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
        })

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)  # Create uploads directory if it doesn't exist
    app.run()
















# import base64
# import requests

# # OpenAI API Key
# api_key = "sk-VVYt9NdbStVVX5LMqnq5ifUZTBa8RzccQQ3OBkcS9kT3BlbkFJgTFUkRLdzqZa-2zOCuCZxPfKtIgmYGhIjlNrKdBfMA"

# # Function to encode an image
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# # Function to analyze multiple base64-encoded images with GPT-4
# def analyze_images_with_gpt4(image_paths):
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {api_key}"
#     }

#     # Prepare the content with multiple image base64 encodings
#     content = [
#         {"type": "text", "text": "You are a profile optimization assistant. Be a bit cocky in your review. Analyze the Hinge profile in the images for the following: 1. Evaluate the quality of the photos (e.g., clarity, lighting, appropriateness for dating apps). 2. Give a rating from 1 to 10 based on the overall profile quality."}
#     ]

#     # Encode each image and add it to the content
#     for image_path in image_paths:
#         base64_image = encode_image(image_path)
#         content.append({
#             "type": "image_url",
#             "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
#         })

#     # Prepare the payload for GPT-4 API
#     payload = {
#         "model": "gpt-4o-mini",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": content
#             }
#         ],
#         "max_tokens": 300
#     }

#     # Send request to GPT-4 API
#     response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

#     # Print the GPT-4 analysis result
#     print(response.json())

# # List of image paths - input your image paths here
# image_paths = [
#     "uploads/IMG_3102.PNG",
#     "uploads/IMG_3103.PNG"
    
# ]

# # Call the function to analyze the images
# analyze_images_with_gpt4(image_paths)
