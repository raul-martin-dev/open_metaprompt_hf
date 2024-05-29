# pip install --upgrade --quiet  text-generation transformers google-search-results numexpr langchainhub sentencepiece jinja2 hugginface_hub
from huggingface_hub.hf_api import HfFolder
from langchain.schema import HumanMessage, AIMessage
import json
import os

HF_TOKEN = os.environ.get("HF_TOKEN", None)


class ModelLoader:
    def __init__(self):
        pass

    def load_openai(self, **kwargs):
        from langchain_openai import ChatOpenAI

        required_args = ['api_key', 'base_url']  # List all relevant arguments
        if not any(kwargs.get(arg) is not None for arg in required_args):
            raise ValueError(f"At least one of {', '.join(required_args)} must be provided")
        
        model = ChatOpenAI(**kwargs)

        return model
    
    def load_huggingface(self, huggingfacehub_api_token, model_name, **kwargs):
        from langchain_community.llms import HuggingFaceEndpoint
        from langchain_community.chat_models.huggingface import ChatHuggingFace

        HfFolder.save_token(huggingfacehub_api_token)

        default_model_kwargs = {
            "task":"text-generation",
            "max_new_tokens": 1000,
            "trust_remote_code": True
        }

        kwargs.update({arg: default for arg, default in default_model_kwargs.items() if arg not in kwargs})
            
        llm = HuggingFaceEndpoint(
            repo_id=model_name,
            huggingfacehub_api_token=huggingfacehub_api_token,
            **kwargs
        )

        model = ChatHuggingFace(llm=llm)

        return model
    
    def load_in_space(self, model_name, **kwargs):
        return self.load_huggingface(HF_TOKEN, model_name, **kwargs)


    
        