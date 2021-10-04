# Don't Buy Alexa! Build Your Own. Create a Virtual Assistant with Python | Python Project | Jarvis AI
# Programming Hero
# https://www.youtube.com/watch?v=AWvsXxDtEkU

# SpeechRecognition 3.8.1
# https://pypi.org/project/SpeechRecognition/, https://github.com/Uberi/speech_recognition
# There is also a fork here: https://pypi.org/project/speech-recognition-fork/
#   pip install SpeechRecognition
import speech_recognition as sr

# pyttsx3 2.90
# https://pypi.org/project/pyttsx3/
#   pip install pyttsx3
import pyttsx3

# PyAudio 0.2.11
# https://pypi.org/project/PyAudio/
# http://people.csail.mit.edu/hubert/pyaudio/docs/
#   pipwin 0.5.1
#   https://pypi.org/project/pipwin/
#   pipwin is a complementary tool for pip on Windows.
#   pipwin installs unofficial python package binaries for windows
#       pip install pipwin
#       pipwin install pyaudio
import pyaudio

# Hotword Detection
#   snowboy 1.2.0b1 - Obsolete
#   https://pypi.org/project/snowboy/
# ALTERNATIVE:
#    pvporcupine 1.9.5
#    https://pypi.org/project/pvporcupine/
#      pip install pvporcupine
#    PPN hotword files are created with Picovoice Console (Account required)
#    https://picovoice.ai/console/
import pvporcupine
from pvrecorder import PvRecorder

# Hotword Commandline Demo
# pvporcupinedemo 1.9.7
# https://pypi.org/project/pvporcupinedemo/
#   pip install pvporcupinedemo
#   Commandline:
#       porcupine_demo_mic --keywords picovoice bumblebee
#       porcupine_demo_mic --show_audio_devices
#         > index: 0, device name: Microphone (Realtek High Definition Audio)
#         > index: 1, device name: Microphone (Sennheiser USB headset)
#         > index: 2, device name: Stereo Mix (Realtek High Definition Audio)

# pywhatkit 5.1
# https://pypi.org/project/pywhatkit/
#   pip install pywhatkit
import pywhatkit


def get_hotword(keywords=None, sensitivities=None):
    """
    Function to wait for user to speak a keyword.

    handle is an instance of Porcupine that detects utterances of a keyword.
    Porcupine can detect multiple keywords concurrently'
    The keywords input argument is a shorthand for accessing the default
    keyword model files (PPN) shipped with the Porcupine package.
    Use print(pvporcupine.KEYWORDS) to see the default keywords.
    The sensitivity of the engine can be tuned per keyword.
    If given the list must be the same length as the keywords list.

    PPN hotword files are created with Picovoice Console
    at https://picovoice.ai/console/ (Account required)

    :param keywords: List of keywords to detect
    :param sensitivities: List of ketword sensitivities
    :return:
    """
    if keywords is None:
        keywords = ['picovoice', 'bumblebee']
    if sensitivities is None:
        sensitivities = [0.5] * len(keywords)

    handle = pvporcupine.create(keywords=keywords, sensitivities=sensitivities)
    recorder = PvRecorder(device_index=1, frame_length=handle.frame_length)
    recorder.start()
    print(f'Waiting for Hotword {keywords} ...')

    while True:
        pcm = recorder.read()
        keyword_index = handle.process(pcm)
        if keyword_index >= 0:
            print(f' Keyword Detected: {keywords[keyword_index]}')
            break

    # When done resources have to be released explicitly
    recorder.stop()
    handle.delete()


def get_devices():
    pya = pyaudio.PyAudio()
    device_count = pya.get_device_count() - 1
    print(f'{device_count = }')

    # Default Devices
    print(pya.get_default_input_device_info())
    print(pya.get_default_output_device_info())


def test_voices(voices):
    for i in range(len(voices)):
        engine.setProperty('voice', voices[i].id)
        talk(f'I am {voices[i].name}')


def talk(text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def get_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
            else:
                print('Alexa was not called.')
    except sr.UnknownValueError:
        command = 'Sorry, I didn\'t understand that.'
    return command


def alexa():
    command = get_command()

    # Play a video on YouTube
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)


def main():
    # rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)

    voices = engine.getProperty('voices')
    # test_voices(voices)
    engine.setProperty('voice', voices[2].id)

    # get_hotword()
    alexa()


if __name__ == '__main__':
    # get_devices()
    engine = pyttsx3.init()
    listener = sr.Recognizer()
    main()
