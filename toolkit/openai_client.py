import openai

class OpenAIClient:
    def __init__(self, api_key_path: str, model: str = "gpt-4o-mini",
                 temperature: float = 0.7, max_completion_tokens: int = 1000,
                 system_prompt: str = "You are a helpful, honest assistant for cleaning and validating CSV files. You are talking to a non-technical user."):
        self.api_key_path = api_key_path
        self.api_key = self._load_api_key()
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.max_completion_tokens = max_completion_tokens
        self.system_prompt = system_prompt

    def _load_api_key(self) -> str:
        with open(self.api_key_path, "r") as f:
            return f.read().strip()
        
    def _ask(self, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_completion_tokens
        )
        
        if not response.choices or not response.choices[0].message.content:
            raise RuntimeError("No response from OpenAI API.")
        
        return response.choices[0].message.content.strip()
    
    def explain_dataset(self, dataset_description: str) -> str:
        prompt = f"Explain the following dataset and its potential issues:\n\n{dataset_description}"
        return self._ask(prompt)


if __name__ == "__main__":
    client = OpenAIClient(api_key_path="api_key", 
                          system_prompt="You are sarcastic and brutally honest.")
    response = client._ask("What happens when you use invalid data in scientific research?")
    print(response)
