import speech_recognition as sr

def live_transcription():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Say something...")

        while True:
            try:
                # Adjust for ambient noise and listen to the microphone with a timeout of 2 seconds
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=3)

                # Use Google Speech Recognition to convert speech to text
                text = recognizer.recognize_google(audio)
                print("You said:", text)

            except sr.UnknownValueError:
                print("Could not understand audio. Please try again.")

            except sr.RequestError as e:
                print(f"Error with the speech recognition service; {e}")

if __name__ == "__main__":
    live_transcription()
