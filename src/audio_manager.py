from playsound import playsound
from config import AUDIO_PATH


def play_audio(func):
    def wrapper():
        playsound(AUDIO_PATH)
        func()

    return wrapper
