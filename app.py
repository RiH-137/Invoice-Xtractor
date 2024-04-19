#IN THIS PROJECT we will use prompt to make a model and that model is itself a model
#  which is trained on invoices and it will generate the response 
# based on the input prompt and the image of the invoice    


from dotenv import load_dotenv
load_dotenv() ## load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## load Gemini pro vision model
model=genai.GenerativeModel('gemini-pro-vision')


#INPUT means instruction to the model   #image means the image of the invoice  #user_prompt means the question asked by the user
def get_gemini_response(input,image,user_prompt):  
    response=model.generate_content([input,image[0],user_prompt])
    return response.text



#conversion of image data into bytes
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title="Invoice Xtractor",page_icon="🧊",layout="centered")

if st.button("About the author"):
    # Display information about the author or code description
    st.write("# About the Author")
    st.write("This Streamlit app is created by Rishi Ranjan.")
    st.write("""
    Date-->  19/04/2024
        🌟 **About Me:**
        https://www.linkedin.com/in/rishi-rih/

🚀 Hey there! I'm Rishi, a passionate 2nd year Computer Science & Engineering Undergraduate with a keen interest in the vast world of technology. Currently specializing in AI and Machine Learning, I'm on a perpetual quest for knowledge and thrive on learning new skills.

💻 My journey in the tech realm revolves around programming, problem-solving, and staying on the cutting edge of emerging technologies. With a strong foundation in Computer Science, I'm driven by the exciting intersection of innovation and research.

🔍 Amidst the digital landscape, I find myself delving into the realms of Blockchain, crafting Android Applications, and ML projects.
 JAVA and Python . 
My GitHub profile (https://github.com/RiH-137) showcases my ongoing commitment to refining my craft and contributing to the tech community.

🏎️ Outside the digital realm, I'm a fervent Formula 1 enthusiast, experiencing the thrill of high-speed pursuits. When I'm not immersed in code or cheering for my favorite F1 team, you might find me strategizing moves on the chessboard.

📧 Feel free to reach out if you're as passionate about technology as I am. You can connect with me at 101rishidsr@gmail.com.

Let's build, innovate, and explore the limitless possibilities of technology together! 🌐✨
        
    
    """)
    if st.button("close"):
        pass

st.header("Invoice Xtractor  🧊")
st.write("Welcome to the Invoice Xtractor.")
st.write("You can ask any questions about the invoice and we will try to answer it.")
st.write("This model can answer in every language and can read invoice of every language.")
input=st.text_input("Enter the query... ",key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices. We will upload a a image as invoice
and you will have to answer any questions based on the uploaded invoice image
"""

## if submit button is clicked

if submit:
    if uploaded_file:
        image_data=input_image_details(uploaded_file)
        response=get_gemini_response(input_prompt,image_data,input)
        st.subheader("The Rresponse is")
        st.write(response)
    else:
        st.error("Please upload the invoice image")

    