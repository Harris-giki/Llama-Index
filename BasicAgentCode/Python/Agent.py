import asyncio
import os
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI

# === Load environment variables ===
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# === Create Gemini LLM ===
llm = GoogleGenAI(
    model="models/gemini-1.5-flash",
    api_key=os.environ["GOOGLE_API_KEY"],
)

# === Main Event Loop ===
async def main():
    print("Gemini Agent Ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("You > ")
        if user_input.strip().lower() in {"exit", "quit"}:
            break
        try:
            response = await llm.acomplete(user_input)
            print("Agent >", str(response))
        except Exception as e:
            print(f"Error: {e}")

# === Entrypoint ===
if __name__ == "__main__":
    asyncio.run(main())