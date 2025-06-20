from RealtimeSTT import AudioToTextRecorder
import pyautogui
import logging

logging.basicConfig(level=logging.INFO)

def process_text(text):
    pyautogui.typewrite(text + " ")

if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder(
        language="en",
        ensure_sentence_starting_uppercase=False,
        ensure_sentence_ends_with_period=False,
        # Using webcam microphone (C922 Pro Stream Webcam)
        # 11 would be pulseaudio
        # Use list_devices.py to find the correct index
        input_device_index=9,
        level=logging.INFO,
    )

    while True:
        recorder.text(process_text)
