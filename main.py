import random
import time
import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

HIGH_SCORE_FILE = "highscore.json"
HISTORY_FILE = "history.json"

SENTENCES = [
    "Python makes coding fun and easy for everyone",
    "Practice typing daily to improve your keyboard speed",
    "Learning new skills requires patience focus and effort",
    "Technology changes rapidly and creates exciting opportunities",
    "Good programmers write clean code with proper structure",
    "Success comes through hard work dedication and consistency"
]


class Root(BoxLayout):

    sentence = StringProperty("")
    result = StringProperty("Ready")
    highscore_text = StringProperty("High Score: 0 WPM")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.start_time = 0
        self.current_sentence = ""

        self.load_highscore()

    def load_highscore(self):
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, "r") as f:
                    data = json.load(f)

                self.highscore_text = (
                    f"High Score: {data['score']} WPM "
                    f"({data['name']})"
                )
            except:
                pass

    def start_test(self):

        self.current_sentence = random.choice(SENTENCES)
        self.sentence = self.current_sentence

        self.ids.typing_input.text = ""

        self.result = "Typing test started..."
        self.start_time = time.time()

    def submit_test(self):

        if not self.current_sentence:
            self.result = "Press Start Test first."
            return

        typed = self.ids.typing_input.text

        elapsed = time.time() - self.start_time

        minutes = elapsed / 60

        words = len(self.current_sentence.split())

        wpm = round(words / minutes) if minutes > 0 else 0

        correct = 0

        for i in range(min(len(typed), len(self.current_sentence))):
            if typed[i] == self.current_sentence[i]:
                correct += 1

        accuracy = (correct / len(self.current_sentence)) * 100

        name = self.ids.name_input.text.strip()

        if not name:
            name = "Anonymous"

        self.save_history(name, wpm, accuracy)
        self.check_highscore(name, wpm)

        self.result = (
            f"Player: {name}\n"
            f"WPM: {wpm}\n"
            f"Accuracy: {accuracy:.2f}%\n"
            f"Time: {elapsed:.2f}s"
        )

    def save_history(self, name, wpm, accuracy):

        history = []

        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    history = json.load(f)
            except:
                history = []

        history.append({
            "name": name,
            "wpm": wpm,
            "accuracy": round(accuracy, 2)
        })

        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=4)

    def check_highscore(self, name, wpm):

        score = 0

        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, "r") as f:
                    score = json.load(f).get("score", 0)
            except:
                pass

        if wpm > score:

            with open(HIGH_SCORE_FILE, "w") as f:
                json.dump(
                    {"name": name, "score": wpm},
                    f,
                    indent=4
                )

            self.highscore_text = (
                f"High Score: {wpm} WPM ({name})"
            )


class TypingMasterApp(App):
    def build(self):
        return Root()


TypingMasterApp().run()
