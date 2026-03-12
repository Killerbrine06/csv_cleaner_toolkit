import logging
import openai

TEMPERATURE = 0.7
MAX_COMPLETION_TOKENS = 500

class OpenAiClient:
    def __init__(self, api_key_path: str, model: str = "gpt-4o-mini", 
                 system_prompt: str = "You are a helpful, honest assistant for cleaning and validating CSV files."):
        self.api_key_path = api_key_path
        self.api_key = self._load_api_key()
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model
        self.system_prompt = system_prompt

    def _load_api_key(self) -> str:
        with open(self.api_key_path, "r") as f:
            return f.read().strip()
        
    def ask(self, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_COMPLETION_TOKENS
            )
        except openai.APIError as e:
            logging.error(f"OpenAI API error: {e}")
            return ""
        
        return response.choices[0].message.content.strip()


if __name__ == "__main__":
    client = OpenAiClient(api_key_path="api_key", 
                          system_prompt="You are sarcastic and brutally honest.")
    response = client.ask("What happens when you use invalid data in scientific research?")
    print(response)
