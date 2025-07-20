import pyttsx3
import speech_recognition as sr
import requests

def speak(text):
    print("AI:", text)
    engine = pyttsx3.init()  # Initialize inside the function
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print("🗣️ You said:", query)
            return query
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, I can't reach the speech service.")
            return ""

def search_duckduckgo(query):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        answer = data.get("AbstractText")
        if not answer:
            answer = "Sorry, I couldn’t find an answer to that."
        return answer
    except Exception as e:
        return f"Error fetching answer: {str(e)}"

def main():
    speak("Hello! I am your AI assistant.")
    while True:
        query = listen().lower()
        if query:
            if "exit" in query or "quit" in query or "stop" in query:
                speak("Goodbye!")
                break
            answer = search_duckduckgo(query)
            speak(answer)

if __name__ == "__main__":
    main()
