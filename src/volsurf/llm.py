from typing import Protocol

from src.volsurf.summary import InstrumentSummary
from src.volsurf.prompts import SYSTEM_PROMPT, build_user_prompt

from anthropic import Anthropic

# ADD TO ENV VARIABLES BEFORE PRODUCTION
ANTHROPIC_API_KEY = "TEST_KEY"

class NarrativeGenerator(Protocol):
  def generate(self, summary: InstrumentSummary) -> str:
    ...

class ClaudeNarrator:
  def __init__(self, model: str | None = None) -> None:
    self.model = model or "claude-sonnet-4-6"
    self.client = Anthropic(api_key=ANTHROPIC_API_KEY)

  def generate(self, summary: InstrumentSummary) -> str:
    response = self.client.messages.create(
      model=self.model,
      system=SYSTEM_PROMPT,
      messages=[{"role": "user", "content": build_user_prompt(summary)}],
      temperature=0.2,
      max_tokens=5000,
    )
    text_blocks = [block.text for block in response.content if getattr(block, "type", None) == "text"]
    text = " ".join(text_blocks).strip()
    
    if not text:
      raise RuntimeError("Claude response was empty.")
    
    return " ".join(text.split())


def build_narrator(model: str | None = None) -> NarrativeGenerator:
  return ClaudeNarrator(model=model)