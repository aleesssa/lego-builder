# Import
from openai import OpenAI
import streamlit as st
import base64
import requests

# INITIALIZE AI models
client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])
# st.title("LEGO Builder")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
picture = st.camera_input("Take a picture")

def to_base64(uploaded_file):
    file_buffer = uploaded_file.read()
    b64 = base64.b64encode(file_buffer).decode()
    return b64

if uploaded_file is not None:
    b64_img = to_base64(uploaded_file)
elif picture is not None:
    b64_img = to_base64(picture)


# response = model.generate_content(["This is the picture", PIL.Image.open("lego.jpg")])

# st.write(response.text)

def analyzeParts():
    headers = {
    'Content-Type' : 'application/json',
    "Authorization" : f'Bearer {st.secrets["OPENAI_API_KEY"]}'
    }
    
    payload = {
        "model" : 'gpt-4o-mini',
        "messages" : [
            {'role' : 'user',
            'content' : [
                {
                    'type' : 'text',
                    'text' : """
                                Analyze the lego parts in the image given. 
                                Identify the type of each lego parts and their quantity.
                                Give the list of the type of lego parts and its quantity 
                                """
                },
                {
                    'type' : 'image_url',
                    'image_url' : { 'url' :f'data:image/png;base64,{b64_img}'}
                }
            ]
            }
        ]}
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response
    


# INPUT

theme = st.text_input("Enter a theme: ")
add_parts = st.checkbox("Additional parts?")
if add_parts:
    budget = st.number_input("Enter your budget for additional parts (RM):")
    prompt_add = f"""You are allowed to add additional parts to the lego model besides the ones that have been provided. 
                    However, take note of the price of each additional part and make sure the total cost should not be greater than RM{budget}.
                    State the overall list of parts required, state which parts are additional and its cost
                    """
else:
    prompt_add = "You are NOT allowed to add additional parts to the lego model besides the ones provided."

system_prompt = f"""
        You are a lego builder.
        You will be provided with a list of lego parts and their quantities.
        You are tasked to generate a lego model together with a step-by-step instruction on how to build it.
        Ensure that the design is physically feasible, using only standard LEGO's assembly logic.
        {prompt_add}
        """


def legoBuilder(legoParts, theme):
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
            {'role' : 'system', 'content' : system_prompt},
            {'role' : 'user', 'content' : f"""Here are the lego parts: {legoParts}
                                                Here is the theme: {theme}
                                            """}
        ]
    )    

    return response
# st.write(system_prompt)

if st.button("Generate"):

    try:
        analyzeParts = analyzeParts().json()
        legoParts = analyzeParts['choices'][0]['message']['content']
        
        legoModel = legoBuilder(legoParts, theme).choices[0].message.content

        st.write(legoModel)
        
            
    except NameError:
        st.write(":red-background[Please upload a file]")
        
        