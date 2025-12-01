# herts.py - Azure Speech to Text with LLM Integration
import os
import sys
import azure.cognitiveservices.speech as speechsdk
from langchain_openai import ChatOpenAI

# Initialize Azure Speech Service credentials
try:
    speech_key = os.environ["AZURE_SPEECH_KEY"]
    region = os.environ["AZURE_SPEECH_REGION"]
except KeyError as e:
    print(f"Error: Missing environment variable {e}. Please set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION.")
    sys.exit(1)

try:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    sys.exit(1)


def transcribe_from_microphone():

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Voice Assistant Started. Say something... (say 'bye' to exit)")

    while True:
        print("\nListening...")
        result = recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            text = result.text.strip()
            print("Transcribed text:", text)

            # Exit conditions
            if text.lower() in ["bye", "exit", "bye herts"]:
                print("Goodbye! Exiting the assistant...")
                break

            # Send to LLM
            response = llm.invoke(text)
            print("LLM response:", response.content)

        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized.")
        else:
            print("Recognition failed:", result.reason)


def transcribe_from_wav(wav_path):

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    audio_input = speechsdk.audio.AudioConfig(filename=wav_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    print(f"Transcribing {wav_path} ...")
    result = recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Transcribed text:", result.text)
    else:
        print("Failed:", result.reason)


if __name__ == "__main__":
    transcribe_from_microphone()
    # transcribe_from_wav("example.wav")
