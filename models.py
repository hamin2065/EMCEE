import os
import anthropic  # For Claude API
import openai  # For GPT API
# from transformers import pipeline  # For Hugging Face models
import transformers
import torch

class APIHandler:
    """Handles API key retrieval and validation for GPT and Claude models."""
    
    @staticmethod
    def get_api_key(service: str) -> str:
        """
        Retrieves the API key for the given service (GPT or Claude).
        
        :param service: "gpt" for OpenAI, "claude" for Anthropic.
        :return: API key if available, otherwise raises an error.
        """
        env_var_map = {
            "gpt": "OPENAI_API_KEY",
            "claude": "ANTHROPIC_API_KEY"
        }
        
        env_var = env_var_map.get(service.lower())
        if not env_var:
            raise ValueError("Unsupported service. Use 'gpt' or 'claude'.")
        
        api_key = os.getenv(env_var)  # Get API key from environment variable
        
        if not api_key:
            raise ValueError(f"Missing API key for {service.upper()}. Please set {env_var} environment variable.")
        
        return api_key

class BaseModel:
    """Base class for AI models with one-shot and few-shot learning support."""
    
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate_response(self, sys_prompt: str, user_prompt: str, examples=None, temp: float = 0.0) -> str:
        """
        Generate a response using one-shot or few-shot prompting.
        
        :param sys_prompt: System instruction (optional)
        :param user_prompt: User's input prompt
        :param examples: List of (input, output) examples for few-shot learning
        :param temp: Temperature for controlling randomness in generation
        :return: Generated response from the model
        """
        raise NotImplementedError("Subclasses must implement this method")

# from api_handler import APIHandler

class GPTModel(BaseModel):
    """Class for interacting with GPT models."""

    def __init__(self, model_name='gpt-4o-mini'):
        super().__init__("GPT")
        self.model_name = model_name
        self.api_key = APIHandler.get_api_key("gpt")  # Ensure API key is provided

    def generate_response(self, sys_prompt: None, user_prompt: str, examples=None, temp: float = 0.0) -> str:
        """Generates response using GPT API."""
        try:
            client = openai.OpenAI(api_key=self.api_key)

            messages = [{"role": "system", "content": sys_prompt}] if sys_prompt else []
            if examples:
                for example in examples:
                    messages.append({"role": "user", "content": example[0]})
                    messages.append({"role": "assistant", "content": example[1]})
            messages.append({"role": "user", "content": user_prompt})
            # print(messages)
            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=1024,
                temperature=temp
            )
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error: {e}"

class ClaudeModel(BaseModel):
    """Class for interacting with Claude models."""

    def __init__(self, model_name='claude-3-5-haiku-20241022'):
        super().__init__("Claude")
        self.model_name = model_name
        self.api_key = APIHandler.get_api_key("claude")  # Ensure API key is provided

    def generate_response(self, sys_prompt: None, user_prompt: str, examples=None, temp: float = 0.0) -> str:
        """Generates response using Claude API."""
        try:
            client = anthropic.Anthropic(api_key=self.api_key)

            messages = [] 
            if examples:
                for example in examples:
                    messages.append({"role": "user", "content": example[0]})
                    messages.append({"role": "assistant", "content": example[1]})
            messages.append({"role": "user", "content": user_prompt})
            if sys_prompt == None:
                message = client.messages.create(
                    model=self.model_name,
                    max_tokens=1024,
                    temperature=temp,
                    messages=messages
                )
            else:
                message = client.messages.create(
                    system = sys_prompt,
                    model=self.model_name,
                    max_tokens=1024,
                    temperature=temp,
                    messages=messages
                )

            return message.content[0].text
        
        except Exception as e:
            return f"Error: {e}"


class LlamaModel(BaseModel):
    """Class for interacting with LLaMA models from Hugging Face."""

    def __init__(self, model_name="meta-llama/Llama-3.1-8B-Instruct"):
        super().__init__("LLaMA-HuggingFace")
        self.model_name = model_name
        self.pipeline = transformers.pipeline(
                            "text-generation",
                            model=model_name,
                            model_kwargs={"torch_dtype": torch.bfloat16},
                            device_map="auto",
                        )

    def generate_response(self, sys_prompt: str, user_prompt: str, examples=None, temp: float = 0.0) -> str:
        """Generates response using Hugging Face LLaMA models."""
        try: 
            messages = []
            if sys_prompt != None:
                messages.append({
                    "role": "system", 
                    "content": sys_prompt
                })
            messages.append({
                "role": "user", 
                "content": user_prompt
            })

            outputs = self.pipeline(
                messages,
                max_new_tokens=256,
            )
            return outputs[0]["generated_text"][-1]['content']
        except Exception as e:
            return f"Error: {e}"