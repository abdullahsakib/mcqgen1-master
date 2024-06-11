import os
import json
import pandas as pd
import traceback
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from src.mcqgen.logger import logging
from src.mcqgen.utils import read_file, get_table_data

import streamlit as st
from src.mcqgen.MCQGenerator import generate_evaluate_chain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
import PyPDF2

with open ("C:\Users\User\Desktop\mcqgen1-master\Response.json",'r') as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQs Creator Application with LangChain 88 ")
with st.form("user_inputs"):
    #File Upload
    uploaded_file=st.file_uploader("Uplaod a PDF or txt file")
    #Input Fields
    mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=50)
    #Subject
    subject=st.text_input("Insert Subject",max_chars=20)
    # Quiz Tone
    tone=st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")
    #Add Button
    button=st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone: 
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
            #Count tokens and the cost of API call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                        "text": text,
                        "number": mcq_count, 
                        "subject": subject, 
                        "tone": tone,
                        "response_json": json.dumps (RESPONSE_JSON)})
                    
            except Exception as e:
                traceback.print_exception (type(e), e, e.__traceback__) 
                st.error("Error")
            else:
                print("Total Tokens: (cb.total_tokens}") 
                print("Prompt Tokens: {cb.prompt_tokens}") 
                print("Completion Tokens: (cb.completion_tokens}") 
                print("Total Cost: (cb.total_cost}")
                if isinstance(response, dict):
                #Extract the quiz data from the response 
                    quiz=response.get("quiz", None)
                    if quiz is not None:
                        table_data=get_table_data(quiz) 
                        if table_data is not None: 
                            df=pd.DataFrame(table_data)
            