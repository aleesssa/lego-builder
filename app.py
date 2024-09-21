# Import
from openai import OpenAI
import google.generativeai as genai
import streamlit as st
import base64
import requests
import PIL.Image

# INITIALIZE AI models
client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

genai.configure(api_key = st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash',
                              system_instruction="""
                                                You will be given a picture of lego parts. 
                                                Analayze the lego parts in the picture. 
                                                Take note of the type of lego part in the picture and their quantities.
                                                Next, come up with a lego model using the said parts and provide a step-by-step instruction on how to build it.
                                                You are not allowed to add any additional parts aside from what is in this picture.
                                                Give output in JSON format. Only provide the JSON format, nothing else.
                                                The JSON must contain:
                                                - short description of lego model 
                                                - lego part(type of lego part, quantity, color)
                                                - steps 
                                                """)

# st.title("LEGO Builder")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
picture = st.camera_input("Take a picture")

# def to_base64(uploaded_file):
#     file_buffer = uploaded_file.read()
#     b64 = base64.b64encode(file_buffer).decode()
#     return b64

if uploaded_file is not None:
    st.image(uploaded_file)
    response = model.generate_content(["This is the picture", PIL.Image.open(uploaded_file)])
    st.write(response.text)
elif picture is not None:
    response = model.generate_content(["This is the picture"], PIL.Image.open(picture))
    


# response = model.generate_content(["This is the picture", PIL.Image.open("lego.jpg")])

# st.write(response.text)

# def analyzeParts():
#     headers = {
#     'Content-Type' : 'application/json',
#     "Authorization" : f'Bearer {st.secrets["OPENAI_API_KEY"]}'
#     }
#     try:
#         payload = {
#             "model" : 'gpt-4o-mini',
#             "messages" : [
#                 {'role' : 'user',
#                 'content' : [
#                     {
#                         'type' : 'text',
#                         'text' : """
#                                  Describe the lego parts in details. Include the type of 
#                                  """
#                     },
#                     {
#                         'type' : 'image_url',
#                         'image_url' : { 'url' :f'data:image/png;base64,{b64_img}'}
#                     }
#                 ]
#                 }
#             ]}
        
#         response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
#         return response
    
#     except NameError:
#         st.write("**:red-background[Please upload or take a picture.]** ")
    

# # INPUT

# theme = st.text_input("Enter a theme : ")
# add_parts = st.checkbox("Additional parts?")
# if add_parts:
#     budget = st.number_input("Enter your budget for additional parts (RM):")
#     prompt_add = f"""You are allowed to add additional parts to the lego model besides the ones that have been provided. 
#                     However, take note of the price of each additional part and make sure the total cost should not be greater than RM{budget}
#                     """
# else:
#     prompt_add = "You are NOT allowed to add additional parts to the lego model besides the ones provided."

# system_prompt = f"""
#         You are a lego builder.
#         You will be provided with a list of lego parts and their quantities, together with a theme.
#         Based on the theme, you are tasked to generate a lego model together with a step-by-step instruction on how to build it.
#         Ensure that the design is physically feasible, using only standard LEGO's assembly logic.
#         Include detailed, step-by-step instructions for each stage of the build, clearly outlining the required pieces for each step, and ensuring that the constructions process is logical, balanced and easy to follow.
#         {prompt_add}
#         """

# st.write(system_prompt)

# def legoBuilder(prompt, theme):
#     response = client.chat.completions.create(
#         model = 'gpt-4o-mini',
#         messages = [
#             {'role' : 'system', 'content' : prompt},
#             {'role' : 'user', 'content' : theme}
#         ]
#     )
    
#     return response.choices[0].message.content

# if st.button("Generate"):
#     try: 
#         response = analyzeParts().json()['choices'][0]['message']['content']
#         userPrompt = f"the theme is {theme}. Here are the lego parts available. {response}"
#         st.write(legoBuilder(system_prompt, userPrompt))
#     except:
#         pass