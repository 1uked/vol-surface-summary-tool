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
  def __init__(self, model: str | None = None, style: str = "default") -> None:
    self.model = model or "claude-sonnet-4-6"
    self.style = style
    self.client = Anthropic(api_key=ANTHROPIC_API_KEY)

  def generate(self, summary: InstrumentSummary) -> str:
    user_prompt = build_user_prompt(summary)
    max_tokens = 5000
    if self.style == "short":
      user_prompt = (
        "Write a short, high-signal summary in 2-3 sentences. "
        "Focus only on the most important points: skew, term structure, liquidity, and major anomalies. "
        "Avoid extra detail and do not speculate.\n\n"
        + user_prompt
      )
      max_tokens = 500

    response = self.client.messages.create(
      model=self.model,
      system=SYSTEM_PROMPT,
      messages=[{"role": "user", "content": user_prompt}],
      temperature=0.2,
      max_tokens=max_tokens,
    )
    text_blocks = [block.text for block in response.content if getattr(block, "type", None) == "text"]
    text = " ".join(text_blocks).strip()
    
    if not text:
      raise RuntimeError("Claude response was empty.")
    
    return " ".join(text.split())


def build_narrator(model: str | None = None, style: str = "default") -> NarrativeGenerator:
  return ClaudeNarrator(model=model, style=style)