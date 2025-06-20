# 🎤 Vibe - Spracherkennung mit Tastatureingabe 🎤

## 🚀 Übersicht

Vibe ist eine Spracherkennungsanwendung, die deine gesprochenen Worte in Echtzeit transkribiert und als Tastatureingaben simuliert. Perfekt für alle, die ihre Hände schonen oder schneller Texte diktieren möchten! 💬✨

## ✨ Funktionen

- 🗣️ **Echtzeit-Spracherkennung** mit dem RealTimeSTT-Framework
- ⌨️ **Automatische Tastatureingabe** der erkannten Sprache
- 🌍 **Unterstützung für Deutsch und Englisch**
- 🖥️ **Wayland-kompatibel** (kein X11 erforderlich)
- 🚀 **CUDA-Beschleunigung** für schnellere Spracherkennung
- 🔤 **Vollständige Unterstützung für deutsche Umlaute** (ä, ö, ü, ß)

## 🛠️ Technische Anforderungen

- Python 3.10+
- CUDA 12+ für GPU-Beschleunigung
- Mikrofon
- Linux mit Wayland oder X11

## 🚀 Installation

```bash
# Repository klonen
git clone https://github.com/sne11ius/vibe.git
cd vibe

# Virtuelle Umgebung mit UV erstellen und aktivieren
uv venv
source .venv/bin/activate

# Abhängigkeiten mit UV installieren
uv pip install -e .
```

## 🎮 Verwendung

1. Starte die Anwendung mit `./vibe`
2. Drücke **F9**, um die Aufnahme zu starten
3. Sprich in dein Mikrofon
4. Lasse **F9** los, um die Aufnahme zu beenden
5. Die erkannte Sprache wird automatisch als Tastatureingabe simuliert

## ⚙️ Konfiguration

Du kannst verschiedene Parameter in der `main.py` anpassen:

- Sprache (`language="de"` oder `language="en"`)
- Modellgröße (`model="medium"` oder andere verfügbare Modelle)
- CUDA-Unterstützung (`device="cuda"` oder `device="cpu"`)
- Mikrofon-Index (`input_device_index=11` - anpassen an dein System)

## 🙌 Beiträge

Beiträge sind willkommen! Öffne einfach einen Pull Request oder ein Issue.

## 📄 Lizenz

[EUPL (European Union Public License) 1.2](LICENSE)
