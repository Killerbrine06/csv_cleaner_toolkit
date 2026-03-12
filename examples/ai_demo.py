from toolkit.openai_client import OpenAIClient

if __name__ == "__main__":
    client = OpenAIClient(api_key_path="api_key", 
                          system_prompt="You are sarcastic and brutally honest.")
    response = client._ask("What happens when you use invalid data in scientific research?")
    print(response)