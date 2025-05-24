import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import json
import os

class MoodEntry:
    def __init__(self, mood, emoji, date=None):
        self.mood = mood
        self.emoji = emoji
        if date:
            self.date = date
        else:
            self.date = datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.now().strftime("%H:%M")

class MoodTracker:
    def __init__(self):
        self.mood_data = {}
        self.selected_mood = ""
        self.load_data()
        self.create_window()

    def create_window(self):
        self.window = tk.Tk()
        self.window.title("Daily Mood Tracker")
        self.window.geometry("550x450")
        self.window.configure(bg='#d6b3ff')  


        title = tk.Label(self.window, text="Daily Mood Tracker",
                        font=('Arial', 20, 'bold'),
                        bg='#d6b3ff', fg='white')
        title.pack(pady=20)

        question = tk.Label(self.window, text="How are you feeling today?",
                           font=('Arial', 14),
                           bg='#d6b3ff', fg='white')
        question.pack(pady=10)

        mood_frame = tk.Frame(self.window, bg='#d6b3ff')
        mood_frame.pack(pady=20)

        self.mood_buttons = []
        moods = [
            ('happy', 'Happy', '😊'),
            ('sad', 'Sad', '😢'),
            ('fearful', 'Fearful', '😨'),
            ('angry', 'Angry', '😠'),
            ('disgusted', 'Disgusted', '🤢'),
            ('calm', 'Calm', '😌')  
        ]

        for i, (mood_id, mood_name, emoji) in enumerate(moods):
            btn = tk.Button(mood_frame,
                           text=f"{emoji}\n{mood_name}",
                           font=('Arial', 11),
                           bg='white',
                           width=8, height=3,
                           command=lambda m=mood_id, e=emoji: self.select_mood(m, e))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.mood_buttons.append(btn)

        self.save_btn = tk.Button(self.window, text="Save",
                                 font=('Arial', 12, 'bold'),
                                 bg='#a066cc', fg='white',
                                 width=15, height=2,
                                 state='disabled',
                                 command=self.save_mood)
        self.save_btn.pack(pady=15)

        history_label = tk.Label(self.window, text="Last 7 Days",
                                font=('Arial', 14, 'bold'),
                                bg='#d6b3ff', fg='white')
        history_label.pack(pady=(10, 5))

        self.history_frame = tk.Frame(self.window, bg='white', width=500, height=150)
        self.history_frame.pack(pady=10, padx=20, fill='both')
        self.history_frame.pack_propagate(False)

        self.show_history()

    def select_mood(self, mood, emoji):
        for btn in self.mood_buttons:
            btn.configure(bg='white')

        for btn in self.mood_buttons:
            if emoji in btn['text']:
                btn.configure(bg='lightgreen')
                break

        self.selected_mood = mood
        self.selected_emoji = emoji
        self.save_btn.configure(state='normal', bg='green')

    def save_mood(self):
        if self.selected_mood == "":
            return

        today = datetime.now().strftime("%Y-%m-%d")

        entry = MoodEntry(self.selected_mood, self.selected_emoji, today)

        self.mood_data[today] = {
            'mood': entry.mood,
            'emoji': entry.emoji,
            'time': entry.time
        }

        self.clean_old_data()

        self.save_data()

        messagebox.showinfo("Success", "Mood saved successfully!")

        self.reset_selection()

        self.show_history()

    def reset_selection(self):
        for btn in self.mood_buttons:
            btn.configure(bg='white')
        self.selected_mood = ""
        self.save_btn.configure(state='disabled', bg='#a066cc')

    def clean_old_data(self):
        week_ago = datetime.now() - timedelta(days=7)
        dates_to_remove = []

        for date_str in self.mood_data.keys():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj < week_ago:
                dates_to_remove.append(date_str)

        for date in dates_to_remove:
            del self.mood_data[date]

    def load_data(self):
        if os.path.exists("mood_data.json"):
            try:
                with open("mood_data.json", "r") as file:
                    self.mood_data = json.load(file)
            except:
                self.mood_data = {}
        else:
            self.mood_data = {}

    def save_data(self):
        with open("mood_data.json", "w") as file:
            json.dump(self.mood_data, file)

    def show_history(self):
        # Clear previous history
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        if len(self.mood_data) == 0:
            no_data_label = tk.Label(self.history_frame, text="No data yet",
                                    font=('Arial', 12), bg='white')
            no_data_label.pack(pady=20)
            return

        sorted_dates = sorted(self.mood_data.keys(), reverse=True)

        for i, date in enumerate(sorted_dates[:7]):
            entry = self.mood_data[date]

            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d.%m.%y")

            entry_text = f"{formatted_date} {entry['mood']}"

            entry_label = tk.Label(self.history_frame, text=entry_text,
                                  font=('Arial', 11), bg='white', fg='black',
                                  anchor='w')
            entry_label.pack(fill='x', padx=10, pady=2)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = MoodTracker()
    app.run()