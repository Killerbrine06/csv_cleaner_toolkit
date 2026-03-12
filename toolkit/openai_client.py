import openai

class OpenAIClient:
    def __init__(self, api_key_path: str, model: str = "gpt-4o-mini",
                 temperature: float = 0.7, max_completion_tokens: int = 1000,
                 system_prompt: str = "You analyze CSV dataset summaries and explain potential data quality issues. You explain problems clearly for non-technical users."):
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
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_completion_tokens
            )
        except Exception as e:
            raise RuntimeError(f"OpenAI API request failed.") from e
        
        if not response.choices or not response.choices[0].message.content:
            raise RuntimeError("No response from OpenAI API.")
        
        return response.choices[0].message.content.strip()
    
    def explain_dataset(self, dataset_description: str) -> str:
        prompt = f"Explain the following dataset and its potential issues:\n\n{dataset_description}"
        return self._ask(prompt)
