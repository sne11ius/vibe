from RealtimeSTT import AudioToTextRecorder
import logging
from pynput import keyboard
from pynput.keyboard import Key, Controller
import time

# Initialize the keyboard controller
keyboard_controller = Controller()


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
    }
    
    for char in text:
        try:
            # First check if it's a direct character we can type
            if char in direct_char_map:
                # Use the direct character mapping
                keyboard_controller.press(direct_char_map[char])
                keyboard_controller.release(direct_char_map[char])
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
            except:
                pass
        
        # Add a small delay between keystrokes
        time.sleep(0.01)

# Usage example:
# type_german_text("Hello! This costs 5€ @ example.com")

# Track key state to prevent repeats
f9_is_pressed = False

logging.basicConfig(level=logging.INFO)

def process_text(text):
    # Type the transcribed text
    type_german_text(text)
    # Explicitly press Enter key after typing the text
    keyboard_controller.press(Key.enter)
    keyboard_controller.release(Key.enter)

if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder(
        device="cuda",
        model="medium",
        language="de",
        ensure_sentence_starting_uppercase=False,
        ensure_sentence_ends_with_period=False,
        input_device_index=11,
        level=logging.INFO,
    )
    def on_key_press(key):
        """Function called when any key is pressed (key down)"""
        global f9_is_pressed

        try:
            if key == keyboard.Key.f9:
                # Only trigger if F9 wasn't already pressed
                if not f9_is_pressed:
                    f9_is_pressed = True
                    print(f"F9 key DOWN at {time.strftime('%H:%M:%S')}")
                    recorder.start()
                    # Add your custom key down logic here
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
                # Add your custom key up logic here
                recorder.stop()
                recorder.text(process_text)
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
