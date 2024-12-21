from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_prompt, image_data, input_text):
    model = genai.GenerativeModel('gemini-pro')
    image_data = image_data[0]
    try:
        response = model.generate_content([input_prompt, image_data, input_text])
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None



def input_image_setup(uploaded_file):
    if uploaded_file is not None and uploaded_file.name:  # Check for filename existence
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        st.error("Please upload an image.")
        return None


st.set_page_config(page_title="Calorie Analyzer")

st.header("Calorie Analyzer App")
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Analyze image")

# Replace with your actual prompt instructions for calorie calculation
input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake,
              along with it it provide whether it is healthy or unhealthy and suggest a tailored exercise routine to 
               burn the calorie intake with the time it will take in the below format

               1. Item 1 - no of calories  healthy or unhealty
               2. Item 2 - no of calories  healthy or unhealty
               ----
               ----
               
               Suggested excercises:
               1. Exercise 1 - for time duration, will burn x calories
               2. Exercise 2 - for time duration, will bun x calories
               -----
               ------


"""

if submit:
    image_data = input_image_setup(uploaded_file)
    if image_data:
        with st.spinner("Analyzing image..."):  # Use a spinner while processing
            response = get_gemini_response(input_prompt, image_data, input_text)
        if response:
            st.subheader("The Calories present are:-")
            st.write(response)
        else:
            st.warning("An error occurred during processing.")