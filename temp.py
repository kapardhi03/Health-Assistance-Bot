import openai
from dotenv import load_dotenv
import os
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Set OpenAI API key
# openai.api_key = os.getenv('OPENAI_API_KEY')

# llm = ChatOpenAI()
llm = ChatOpenAI(openai_api_key="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")


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])
output_parser = StrOutputParser()
# x=llm.invoke("how can langsmith help with testing?")
# print(type(x))
# print(x)


chain = prompt | llm | output_parser
y=chain.invoke({"input": "how can langsmith help with testing?"})

print(y)
#
# chatbot = OpenAI(api_key=openai.api_key, model="text-davinci-003")

# def chat_with_bot(prompt):
    
#     response = chatbot.run(prompt)
#     return response


# if _name_ == "_main_":
#     user_input = "Tell me a joke."
#     response = chat_with_bot(user_input)
#     print(f"Chatbot: {response}")