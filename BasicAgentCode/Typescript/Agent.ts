import "dotenv/config";
import { agent } from "@llamaindex/workflow";
import { Settings } from "llamaindex";
import { gemini, GEMINI_MODEL } from "@llamaindex/google";

async function main() {
  // Set global LLM (optional, but useful for consistency)
  Settings.llm = gemini({
    apiKey: process.env.GOOGLE_API_KEY,
    model: GEMINI_MODEL.GEMINI_2_0_FLASH,
  });

  // Create a minimal agent without tools
  const myAgent = agent({
    systemPrompt: "your name is bobby lashly", // this is setting the role of the llm
  });

  let prompt: string = "who are you?";
  // Run the agent
  const response = await myAgent.run(prompt);
  console.log(response.data.message);
}

main();
