from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Ensure the API key is correctly set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-pro-vision")

def get_response(prompt, image, input):
    try:
        response = model.generate_content([prompt, image[0], input])
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Gemini Nutritionist")

st.header("Gemini Nutritionist")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the Food...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert nutritionist. You need to see the food items from the image
and calculate the total calories. Also, provide the details of every food item with calorie intake
in the following format:
1. Item 1 - number of calories
2. Item 2 - number of calories
----
-----

Finally, mention whether the food is healthy or not and also mention the percentage split of the ratio of carbohydrates, fats, fibers, sugars, and 
other things required in our diet. You should recommend a better diet than the image.
"""

# If submit button is clicked
if submit:
    try:
        image_data = input_image_details(uploaded_file)
        response = get_response(input_prompt, image_data, input)
        if response:
            st.subheader("The Response is")
            st.write(response)
    except Exception as e:
        st.error(f"Error processing the request: {e}")