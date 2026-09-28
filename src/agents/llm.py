import os
from openai import OpenAI

class LocalLLM:
    """Chat client for an open-source model served locally by oMLX (OpenAI-compatible API)."""

    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv('OMLX_BASE_URL', 'http://localhost:8000/v1'),
            api_key=os.environ['OMLX_API_KEY'],
        )
        self.model = os.environ['OMLX_MODEL']
        # Qwen "thinking" is slow but better for hard problems; off unless OMLX_THINKING is set
        self.thinking = os.getenv('OMLX_THINKING', 'false').lower() in ('1', 'true', 'yes', 'on')

    def chat(self, system: str, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            extra_body={"chat_template_kwargs": {"enable_thinking": self.thinking}},
        )
        return response.choices[0].message.content
