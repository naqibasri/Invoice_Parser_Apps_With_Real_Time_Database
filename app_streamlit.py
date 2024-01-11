# Q&A Chatbot
#from langchain.llms import OpenAI

from logging import info
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    return response.text
    

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
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


##initialize our streamlit app

st.set_page_config(page_title="INVOICE PARSER APPS")
def parser():
    st.header("INVOICE PARSER APPS")
    #input=st.text_input("Input Prompt: ",key="input")
    uploaded_file = st.file_uploader("Choose an invoice...", type=["jpg", "jpeg", "png"])
    image=""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)


    submit=st.button("Parse the invoice")

    input_prompt = """
                   You are an invoice parser.
                   You will receive input images as invoices &
                   you need to provide the value based on the input invoice. 
                   """

    ## If ask button is clicked
    question = {'InvoiceNum':"What is the invoice number? please just give me the value only",
                'InvoiceDate':"What is the invoice date? please just give me the value only",
                'InvoiceItem':'Can you provide a list of dicts of the item name, quantity and price of each of the items listed in the invoice. Please give in the format[{"name": "Rubber","quantity": 1,"price": 270.0},...]',
                'InvoiceDiscount':"Can you provide the amount of discount in the invoice if any. If not available, please return 0",
                'InvoiceTotal':"What is the final amount of the invoice after discount and taxes? please just give me the value only"}
    if submit:
        responses=[]
        image_data = input_image_setup(uploaded_file)
        for info in question:
            response=get_gemini_response(input_prompt,image_data,question[info])
            responses.append(response)
            #st.subheader("The Response is")
        for response in responses:
            st.write(response) 

def database():
    st.header("CHECK YOUR CURRENT DATABASE HERE")
    
def analysis():
    st.header("CHECK YOUR ANALYSIS HERE")

def main():
    pages = {
        "parser": parser,
        "database": database,
        "analysis": analysis
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.selectbox("Go to", list(pages.keys()), format_func=str.upper)

    page = pages[selection]
    page()

if __name__ == "__main__":
    main()