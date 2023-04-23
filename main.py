import requests
from gtts import gTTS
import speech_recognition as sr
from key import api_key

def generate_text(prompt):
    
    url = "https://api.openai.com/v1/engines/davinci/completions"
    api_key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 2030,
        "n": 1,
        "stop": None,
        "temperature": 2
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print(f"Erro na requisição: {response.status_code}")
        print(response.text)
        return None

    response_json = response.json()

    if "choices" not in response_json:
        print("A resposta não contém a chave 'choices'.")
        return None

    generated_text = response_json["choices"][0]["text"]
    return generated_text

if __name__ == "__main__":
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escutando...")
        audio = r.listen(source)

    try:
        text_prompt = r.recognize_google(audio)
        print("O reconhecimento de voz entendeu: " + text_prompt)
    except sr.UnknownValueError:
        print("O reconhecimento de voz não entendeu nada...")
        text_prompt = None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        text_prompt = None

    if text_prompt:
        result = generate_text(text_prompt)
        if result:
            print(result)
        else:
            print("Não foi possível gerar o texto.")
    else:
        print("Não foi possível converter o áudio em texto.")


tts = gTTS(result)
tts.save('audios/response.mp3')