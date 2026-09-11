from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

response = client.responses.create(
    model="gpt-5-mini",
    input="AI Agent를 한문장으로 설명해줘."
)

print(response.output_text)