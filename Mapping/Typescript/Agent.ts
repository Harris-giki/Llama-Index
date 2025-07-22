import "dotenv/config";
import { agent } from "@llamaindex/workflow";
import { tool, Settings } from "llamaindex";
import { gemini, GEMINI_MODEL } from "@llamaindex/google";
import { z } from "zod";

async function main() {
  // Set the global LLM (GPT-4o) with API key
  Settings.llm = gemini({
    apiKey: process.env.GOOGLE_API_KEY,
    model: GEMINI_MODEL.GEMINI_2_0_FLASH,
  });
  // Tool function to add two numbers
  const sumNumbers = ({ a, b }: { a: number; b: number }): string => {
    return `${a + b}`;
  };

  // Define tool schema and behavior
  const addTool = tool({
    name: "sumNumbers",
    description: "Use this function to sum two numbers",
    parameters: z.object({
      a: z.number({ description: "First number to sum" }),
      b: z.number({ description: "Second number to sum" }),
    }),
    execute: sumNumbers,
  });

  // Register the tool with the agent
  const tools = [addTool];
  const myAgent = agent({ tools });

  // Run the agent with a natural language prompt
  const result = await myAgent.run("Sum 101 and 303");
  console.log(result.data);
}

main().catch(console.error);
