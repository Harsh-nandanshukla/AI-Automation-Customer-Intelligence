from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# Load variables from .env
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# Test call
response = llm.invoke("Hello!")

print(response.content)