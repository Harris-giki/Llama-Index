import asyncio
import google.generativeai as genai
from llama_index.llms.base import LLM
from llama_index.core.agent.workflow import FunctionAgent
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


# === Custom Gemini Wrapper for LlamaIndex ===
class GeminiLLM(LLM):
    def __init__(self, model_name: str = "models/gemini-pro"):
        # Instantiate the Gemini model using the Google Generative AI SDK
        self.model = genai.GenerativeModel(model_name)

    async def _acall(self, prompt: str, **kwargs) -> str:
        """
        Async version of the `call` method.
        Since Gemini API is synchronous, this offloads it to a thread.
        """
        return await asyncio.to_thread(self.call, prompt)

    def call(self, prompt: str) -> str:
        """
        Synchronously generate a response from Gemini using the prompt.
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()

    @property
    def metadata(self):
        return {
            "model_name": "gemini-pro",
            "is_chat_model": True
        }


# === Tool Function ===
def multiply(a: float, b: float) -> float:
    """Useful for multiplying two numbers."""
    return a * b


# === Create LlamaIndex Function Agent ===
agent = FunctionAgent(
    tools=[multiply],
    llm=GeminiLLM(),
    system_prompt="You are a helpful assistant that can multiply two numbers."
)


# === Main Event Loop ===
async def main():
    print("Gemini Agent Ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("You > ")
        if user_input.strip().lower() in {"exit", "quit"}:
            break
        try:
            response = await agent.run(user_input)
            print("Agent >", str(response))
        except Exception as e:
            print(f"Error: {e}")


# === Entrypoint ===
if __name__ == "__main__":
    asyncio.run(main())
