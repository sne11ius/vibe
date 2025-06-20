import pyaudio

p = pyaudio.PyAudio()

print("Available audio input devices:")
print("-" * 50)

for i in range(p.get_device_count()):
    dev_info = p.get_device_info_by_index(i)
    if dev_info['maxInputChannels'] > 0:  # Only show devices with input capability
        print(f"Device {i}: {dev_info['name']}")
        print(f"  Input channels: {dev_info['maxInputChannels']}")
        print(f"  Default sample rate: {dev_info['defaultSampleRate']}")
        print()

p.terminate()
