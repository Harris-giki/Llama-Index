import asyncio
import google.generativeai as genai
from llama_index.llms.base import LLM
from llama_index.core.agent.workflow import FunctionAgent
from typing import Optional
import os