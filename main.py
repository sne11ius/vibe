from RealtimeSTT import AudioToTextRecorder
import logging
from pynput import keyboard
from pynput.keyboard import Key, Controller
import time
import sys
import sounddevice as sd
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

# Initialize the keyboard controller
keyboard_controller = Controller()


class AudioDeviceSelector(QDialog):
    """Dialog zur Auswahl des Audioeingabegeräts mit Buttons"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_device_index = None
        self.setWindowTitle("🎤 Vibe - Audioeingabegerät auswählen")
        self.setMinimumWidth(500)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Titel
        title_label = QLabel("<h2>Vibe Spracherkennung</h2>")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Erklärungstext
        info_label = QLabel("<b>Wählen Sie Ihr Mikrofon mit einem Klick:</b>")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        # Geräteliste abrufen
        devices = sd.query_devices()
        input_devices = []
        
        # Nur Eingabegeräte anzeigen
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                name = f"{device['name']}"
                channels = device['max_input_channels']
                input_devices.append((i, name, channels))
        
        # Buttons für jedes Gerät erstellen
        self.buttons_group = QVBoxLayout()
        self.selected_device_index = None
        
        # Standardgerät (für Hervorhebung)
        default_index = 11
        
        # Buttons für jedes Gerät erstellen
        for idx, name, channels in input_devices:
            # Button mit Geräteinformationen
            device_button = QPushButton(f"🎙️ {name}\nKanäle: {channels} | Index: {idx}")
            device_button.setMinimumHeight(60)  # Höhere Buttons für bessere Klickbarkeit
            
            # Stil für bessere Sichtbarkeit
            if idx == default_index:
                device_button.setStyleSheet(
                    "QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }"
                    "QPushButton:hover { background-color: #45a049; }"
                )
            else:
                device_button.setStyleSheet(
                    "QPushButton { background-color: #f0f0f0; }"
                    "QPushButton:hover { background-color: #e0e0e0; }"
                )
            
            # Funktion zum Auswählen und Schließen
            def make_device_selector(device_idx):
                def select_device():
                    self.selected_device_index = device_idx
                    self.accept()
                return select_device
            
            device_button.clicked.connect(make_device_selector(idx))
            self.buttons_group.addWidget(device_button)
        
        layout.addLayout(self.buttons_group)
        
        # Abbrechen-Button unten
        cancel_button = QPushButton("Abbrechen")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("QPushButton { color: #f44336; }")
        layout.addWidget(cancel_button)
        
        self.setLayout(layout)
    
    def get_selected_device(self):
        """Gibt den Index des ausgewählten Geräts zurück"""
        return self.selected_device_index


# Complete German QWERTZ to US QWERTY character mapping
german_char_map = {
    # Basic letter swaps - commented out as we're using US layout
    # 'z': 'y',
    # 'y': 'z',

    # Number row special characters (Shift + number)
    '!': ['shift', '1'],    # Same as US
    '"': ['shift', '2'],    # German: Shift+2 = ", US: Shift+2 = @
    '§': ['shift', '3'],    # German only: Shift+3 = §
    '$': ['shift', '4'],    # Same as US
    '%': ['shift', '5'],    # Same as US
    '&': ['shift', '6'],    # Same as US
    '/': ['shift', '7'],    # German: Shift+7 = /, US: Shift+7 = &
    '(': ['shift', '8'],    # Same as US
    ')': ['shift', '9'],    # Same as US
    '=': ['shift', '0'],    # German: Shift+0 = =, US: Shift+0 = )
    '?': ['shift', 'minus'], # German: Shift+ß = ?, US: Shift+- = _

    # Special German characters on number row (no shift)
    'ß': 'minus',           # German ß is where US - is
    '´': 'equal',           # German ´ is where US = is

    # Top row special characters
    'ü': 'bracketleft',     # German ü is where US [ is
    '+': 'bracketright',    # German + is where US ] is
    'Ü': ['shift', 'bracketleft'],   # Shift+ü = Ü
    '*': ['shift', 'bracketright'],  # German: Shift++ = *

    # Middle row special characters  
    'ö': 'semicolon',       # German ö is where US ; is
    'ä': 'apostrophe',      # German ä is where US ' is
    'Ö': ['shift', 'semicolon'],     # Shift+ö = Ö
    'Ä': ['shift', 'apostrophe'],    # Shift+ä = Ä

    # Bottom row special characters
    '<': 'backslash',       # German < is where US \ is (next to left shift)
    '>': ['shift', 'backslash'],     # German: Shift+< = >
    '|': ['altgr', 'backslash'],     # German: AltGr+< = |

    # Characters requiring AltGr on German keyboard
    '@': ['altgr', 'q'],    # AltGr+Q = @
    '€': ['altgr', 'e'],    # AltGr+E = €
    '{': ['altgr', '7'],    # AltGr+7 = {
    '[': ['altgr', '8'],    # AltGr+8 = [
    ']': ['altgr', '9'],    # AltGr+9 = ]
    '}': ['altgr', '0'],    # AltGr+0 = }
    '\\': ['altgr', 'minus'], # AltGr+ß = \
    '~': ['altgr', 'plus'],   # AltGr++ = ~
    '²': ['altgr', '2'],    # AltGr+2 = ²
    '³': ['altgr', '3'],    # AltGr+3 = ³
    '¼': ['altgr', '4'],    # AltGr+4 = ¼
    '½': ['altgr', '5'],    # AltGr+5 = ½
    '¾': ['altgr', '6'],    # AltGr+6 = ¾
    '¬': ['altgr', '7'],    # AltGr+7 = ¬ (alternative)
    '¦': ['altgr', 'backslash'], # AltGr+< = ¦ (alternative)

    # Characters that produce different results
    '#': 'numbersign',      # German # key produces ' on US layout
    "'": 'numbersign',      # German ' is on # key position
    '^': 'grave',           # German ^ is where US ` is (dead key)
    '°': ['shift', 'grave'], # German: Shift+^ = °

    # Punctuation differences
    ',': 'comma',           # Same position
    '.': 'period',          # Same position  
    '-': 'slash',           # German - is where US / is
    '_': ['shift', 'slash'], # German: Shift+- = _
    ':': ['shift', 'period'], # German: Shift+. = :
    ';': ['shift', 'comma'],  # German: Shift+, = ;
}

def type_german_text(text):
    """Type text correctly on German keyboard layout using pynput"""
    # Define a simplified mapping for special keys
    # We'll just use character-by-character typing for most keys
    special_key_map = {
        'space': ' ',
        'period': '.',
        'comma': ',',
        'slash': '/',
        'backslash': '\\',
        'semicolon': ';',
        'apostrophe': "'",  # This is the key for apostrophe/single quote
        'bracketleft': '[',
        'bracketright': ']',
        'minus': '-',
        'equal': '=',
        'grave': '`',
        'numbersign': '#',
    }
    
    # Add direct character mappings for common special characters
    direct_char_map = {
        "'": "'",  # Apostrophe/single quote
        '"': '"',  # Double quote
        '!': '!',   # Exclamation mark
        '?': '?',   # Question mark
        '.': '.',   # Period
        ',': ',',   # Comma
        ';': ';',   # Semicolon
        ':': ':',   # Colon
        '@': '@',   # At symbol
        '#': '#',   # Hash/pound
        '$': '$',   # Dollar
        '%': '%',   # Percent
        '^': '^',   # Caret
        '&': '&',   # Ampersand
        '*': '*',   # Asterisk
        '(': '(',   # Open parenthesis
        ')': ')',   # Close parenthesis
        '-': '-',   # Hyphen/minus
        '_': '_',   # Underscore
        '+': '+',   # Plus
        '=': '=',   # Equals
        '[': '[',   # Open square bracket
        ']': ']',   # Close square bracket
        '{': '{',   # Open curly brace
        '}': '}',   # Close curly brace
        '|': '|',   # Pipe
        '\\': '\\', # Backslash
        '/': '/',   # Forward slash
        '<': '<',   # Less than
        '>': '>',   # Greater than
        '`': '`',   # Backtick
        '~': '~',   # Tilde
        # Deutsche Umlaute
        'ä': 'ä',   # a umlaut
        'ö': 'ö',   # o umlaut
        'ü': 'ü',   # u umlaut
        'ß': 'ß',   # eszett
        'Ä': 'Ä',   # A umlaut
        'Ö': 'Ö',   # O umlaut
        'Ü': 'Ü',   # U umlaut
    }
    
    for char in text:
        try:
            # First check if it's a direct character we can type
            if char in direct_char_map:
                # Use the direct character mapping
                keyboard_controller.press(direct_char_map[char])
                keyboard_controller.release(direct_char_map[char])
            # Special handling for German umlauts
            elif char in ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']:
                # Try multiple approaches for umlauts
                try:
                    # First try direct typing
                    keyboard_controller.type(char)
                except Exception:
                    try:
                        # Then try press/release
                        keyboard_controller.press(char)
                        keyboard_controller.release(char)
                    except Exception:
                        # If all else fails, print a warning
                        print(f"Warning: Could not type umlaut '{char}'")
            elif char in german_char_map:
                key_combo = german_char_map[char]
                if isinstance(key_combo, list):
                    # Handle modifier keys (shift, altgr, etc.)
                    if key_combo[0] == 'shift':
                        # For shift combinations, we'll directly type the shifted character
                        # if it's in our special key map
                        if key_combo[1] in special_key_map:
                            # Type the character directly
                            keyboard_controller.press(Key.shift)
                            keyboard_controller.press(special_key_map[key_combo[1]])
                            keyboard_controller.release(special_key_map[key_combo[1]])
                            keyboard_controller.release(Key.shift)
                        else:
                            # Just type the character directly
                            keyboard_controller.press(Key.shift)
                            keyboard_controller.press(key_combo[1])
                            keyboard_controller.release(key_combo[1])
                            keyboard_controller.release(Key.shift)
                    elif key_combo[0] == 'altgr':
                        # For AltGr combinations, we'll try to use the character directly
                        # if possible, otherwise skip it
                        print(f"Warning: AltGr combination for '{char}' might not work on Wayland")
                        # Just try to type the character directly
                        keyboard_controller.press(char)
                        keyboard_controller.release(char)
                else:
                    # Handle single keys by using our special key map
                    if key_combo in special_key_map:
                        # Type the mapped character directly
                        keyboard_controller.press(special_key_map[key_combo])
                        keyboard_controller.release(special_key_map[key_combo])
                    else:
                        # Just try to type the key directly
                        keyboard_controller.press(key_combo)
                        keyboard_controller.release(key_combo)
            else:
                # For regular letters and numbers that are the same
                keyboard_controller.press(char)
                keyboard_controller.release(char)
        except Exception as e:
            print(f"Warning: Could not type '{char}': {str(e)}")
            # Try to type the character directly as a fallback
            try:
                keyboard_controller.type(char)
            except Exception:
                # Last resort: try to map umlauts to their ASCII equivalents
                umlaut_map = {
                    'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
                    'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue'
                }
                if char in umlaut_map:
                    for replacement_char in umlaut_map[char]:
                        try:
                            keyboard_controller.press(replacement_char)
                            keyboard_controller.release(replacement_char)
                        except Exception:
                            pass
        
        # Add a small delay between keystrokes
        time.sleep(0.01)

# Usage example:
# type_german_text("Hello! This costs 5€ @ example.com")

# Track key state to prevent repeats
f9_is_pressed = False

logging.basicConfig(level=logging.INFO)

def process_text(text):
    # Check if we got any text to process
    if not text or text.strip() == "":
        print("⚠️ Keine Sprache erkannt. Bitte versuchen Sie es erneut.")
        return
        
    print(f"📝 Erkannter Text: '{text}'")
    
    # Type the transcribed text
    try:
        type_german_text(text)
        # Explicitly press Enter key after typing the text
        keyboard_controller.press(Key.enter)
        keyboard_controller.release(Key.enter)
    except Exception as e:
        print(f"❌ Fehler beim Tippen des Textes: {str(e)}")


if __name__ == '__main__':
    print("Vibe Spracherkennung wird initialisiert...")
    
    # GUI-Anwendung initialisieren
    app = QApplication(sys.argv)
    
    # Dialog zur Geräteauswahl anzeigen
    device_selector = AudioDeviceSelector()
    if device_selector.exec_() != QDialog.Accepted:
        print("Abgebrochen. Beende Anwendung.")
        sys.exit(0)
    
    # Ausgewähltes Gerät abrufen
    selected_device = device_selector.get_selected_device()
    if selected_device is None:
        print("Kein Gerät ausgewählt. Beende Anwendung.")
        sys.exit(0)
    
    print(f"🎙️ Ausgewähltes Mikrofon: Index {selected_device}")
    
    # Geräteinformationen anzeigen
    try:
        devices = sd.query_devices()
        device_info = devices[selected_device]
        print(f"Gerätname: {device_info['name']}")
        print(f"Kanäle: {device_info['max_input_channels']}")
    except Exception as e:
        print(f"Konnte Geräteinformationen nicht abrufen: {e}")

    
    try:
        # Try to use CUDA first
        recorder = AudioToTextRecorder(
            model="medium",  # Use the multilingual model
            language="de",   # Set language to German
            device="cuda",   # Use CUDA for faster processing
            input_device_index=selected_device,  # Use selected microphone device
            ensure_sentence_starting_uppercase=False,
            ensure_sentence_ends_with_period=False,
            level=logging.INFO,
        )
        print("✅ CUDA device erfolgreich initialisiert.")
    except Exception as e:
        print(f"⚠️ CUDA konnte nicht initialisiert werden: {str(e)}")
        print("Fallback auf CPU...")
        # Fallback to CPU if CUDA is not available
        recorder = AudioToTextRecorder(
            model="medium",  # Use the multilingual model
            language="de",   # Set language to German
            device="cpu",    # Fallback to CPU
            input_device_index=selected_device,  # Use selected microphone device
            ensure_sentence_starting_uppercase=False,
            ensure_sentence_ends_with_period=False,
            level=logging.INFO,
        )
        print("✅ CPU-Modus aktiviert.")
    print("Drücke F9, um die Aufnahme zu starten und loszulassen, um zu transkribieren.")

    def on_key_press(key):
        """Function called when any key is pressed (key down)"""
        global f9_is_pressed

        try:
            if key == keyboard.Key.f9:
                # Only trigger if F9 wasn't already pressed
                if not f9_is_pressed:
                    print("F9 key DOWN at %s" % time.strftime("%H:%M:%S"))
                    print("🎤 Aufnahme gestartet - sprechen Sie jetzt...")
                    f9_is_pressed = True
                    recorder.start()
                    return True           # Add your custom key down logic here
        except AttributeError:
            # Special keys (like F9) are handled above
            pass
    def on_key_release(key):
        """Function called when any key is released (key up)"""
        global f9_is_pressed

        try:
            if key == keyboard.Key.f9:
                f9_is_pressed = False
                print(f"F9 key UP at {time.strftime('%H:%M:%S')}")
                print("💬 Transkribiere Sprache...")
                recorder.stop()
                recorder.text(process_text)
                print("✨ Transkription abgeschlossen.")

        except AttributeError:
            # Special keys (like F9) are handled above
            pass

    try:
        # Start the listener with both press and release callbacks
        with keyboard.Listener(
            on_press=on_key_press,
            on_release=on_key_release
        ) as listener:
            listener.join()

    except KeyboardInterrupt:
        print("\nExiting...")
