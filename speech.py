import speech_recognition as sr




def listen_to_mic(timeout=10, phrase_time_limit=15): 
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8
    recognizer.non_speaking_duration = 0.5

    try:
        with sr.Microphone() as source:
            # print("Listening... calibrating microphone for ambient noise...")
            # recognizer.adjust_for_ambient_noise(source, duration=2) this was suggested from ai and seems very redundant
            print("Listening... please speak.")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        text = recognizer.recognize_google(audio, language="de-DE")        
        return text
    
    except sr.WaitTimeoutError:
        print("No speech detected - timeout while waiting for phrase to start.")
        return ""
    except sr.UnknownValueError:
        print("Could not understand audio - try speaking more clearly.")
        return ""
    except sr.RequestError as e:
        print(f"Speech API error (check internet connection): {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error: {e}")
        return ""

if __name__ == "__main__":
    result = listen_to_mic()
    print("You said:", result or "no text recognized.")