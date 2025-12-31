import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

groq_api_key=os.getenv("GROQ_API_KEY")

llm=ChatGroq(groq_api_key=groq_api_key,model="Llama3-8b-8192")
llm

class LLMClient:

    def __init__(self, model_name="qwen/qwen3-32b"):
        self.llm_model = ChatGroq(
            model=model_name,
            temperature=0,
            max_tokens=None,
            reasoning_format="parsed",
            timeout=None,
            max_retries=2,
            # other params...
        )

    def generate(self, prompt: str):
        response = self.llm_model.invoke(prompt)
        return response