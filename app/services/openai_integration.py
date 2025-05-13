import openai
import os

# Configure sua chave API
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_job_suggestions(text: str) -> str:
    prompt = f"Analise o currículo a seguir e sugira 3 vagas ideais para o candidato, baseando-se nas habilidades e experiência mencionadas: {text}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",  # Escolha o modelo que achar melhor
        prompt=prompt,
        max_tokens=150
    )
    
    return response.choices[0].text.strip()
