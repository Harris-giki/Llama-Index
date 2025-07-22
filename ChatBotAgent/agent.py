import asyncio
import os
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool

# === Load environment variables ===
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# === Create Tool Functions ===
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the product."""
    return a * b

def add(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b

# === Wrap functions as LlamaIndex tools ===
multiply_tool = FunctionTool.from_defaults(fn=multiply)
add_tool = FunctionTool.from_defaults(fn=add)

# === Create Gemini LLM ===
llm = GoogleGenAI(
    model="models/gemini-1.5-flash",
    api_key=os.environ["GOOGLE_API_KEY"]
)

# === Create Function Agent ===
workflow = FunctionAgent(
    tools=[multiply_tool, add_tool],
    llm=llm,
    system_prompt="You are an agent that can perform basic mathematical operations using tools."
)

# === Main Event Loop ===
async def main():
    print("Gemini Agent Ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("You > ")
        if user_input.strip().lower() in {"exit", "quit"}:
            break
        try:
            response = await workflow.run(user_msg=user_input)
            print("Agent >", str(response))
        except Exception as e:
            print(f"Error: {e}")

# === Entrypoint ===
if __name__ == "__main__":
    asyncio.run(main())