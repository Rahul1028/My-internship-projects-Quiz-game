import random
import tkinter as tk
from tkinter import messagebox

class QuizHistory:
    @staticmethod
    def save_participant_details(name, age):
        with open("participant_history.txt", "a") as file:
            file.write(f"Name: {name}, Age: {age}\n")

    @staticmethod
    def save_quiz_result(score, total_questions):
        with open("participant_history.txt", "a") as file:
            file.write(f"Score: {score}/{total_questions}\n")

class ParticipantDetailsPage:
    def __init__(self, master, start_quiz_callback):
        self.master = master
        self.start_quiz_callback = start_quiz_callback

        # Set background color
        master.configure(bg='light blue')  # Change to your preferred color

        self.title_label = tk.Label(master, text="Participant Details", font=("Poppins", 18, "bold"), bg='light blue')
        self.title_label.pack(pady=20)

        self.name_label = tk.Label(master, text="Enter Your Name:", font=("Poppins", 12), bg='light blue')
        self.name_label.pack()

        self.name_entry = tk.Entry(master, font=("Poppins", 12))
        self.name_entry.pack(pady=10)

        self.age_label = tk.Label(master, text="Enter Your Age:", font=("Poppins", 12), bg='light blue')
        self.age_label.pack()

        self.age_entry = tk.Entry(master, font=("Poppins", 12))
        self.age_entry.pack(pady=10)

        self.start_button = tk.Button(master, text="Start Quiz", command=self.start_quiz, font=("Poppins", 14))
        self.start_button.pack(pady=10)

    def start_quiz(self):
        participant_name = self.name_entry.get()
        participant_age = self.age_entry.get()

        if not participant_name or not participant_age or not participant_age.isdigit():
            messagebox.showerror("Error", "Please enter valid participant details.")
            return

        QuizHistory.save_participant_details(participant_name, participant_age)

        self.master.destroy()
        quiz_game = QuizGame(questions_data, participant_name, int(participant_age))
        quiz_game.start_game()

class QuizGame:
    def __init__(self, questions, participant_name, participant_age):
        self.questions = questions
        self.participant_name = participant_name
        self.participant_age = participant_age
        self.score = 0
        self.current_question = 0
        self.attempted_questions = 0
        self.timer_seconds = 10

        self.root = tk.Tk()
        self.root.title("Python: SR Quiz Game")

        # Set background color
        self.root.configure(bg='light blue')  # Change to your preferred color
        # Set window size to fit the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.root.geometry(f"{window_width}x{window_height}")

        self.question_label = tk.Label(self.root, text="", font=("Poppins", 12), bg='light blue')  # Change background color
        self.question_label.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self.root, text="", font=("Poppins", 12), command=lambda i=i: self.check_and_submit(i + 1), state=tk.DISABLED)
            button.pack(pady=5)
            self.option_buttons.append(button)

        self.user_answer = tk.StringVar()
        entry_label = tk.Label(self.root, text="Enter your answer:", font=("Poppins", 12), bg='light blue')  # Change background color
        entry_label.pack()
        self.entry = tk.Entry(self.root, textvariable=self.user_answer, font=("Poppins", 12))
        self.entry.pack()

        self.timer_label = tk.StringVar()
        timer_display = tk.Label(self.root, textvariable=self.timer_label, font=("Poppins", 12, "italic"), bg='light blue')  # Change background color
        timer_display.pack(pady=10)

        self.question_info_label = tk.Label(self.root, text="Questions: 0", font=("Poppins", 12), bg='light blue')
        self.question_info_label.pack(side=tk.RIGHT, padx=20)

        self.attempted_info_label = tk.Label(self.root, text="Attempted: 0", font=("Poppins", 12), bg='light blue')
        self.attempted_info_label.pack(side=tk.RIGHT, padx=20)

        self.lifelines_used = {"50-50": False, "Ask the Audience": False}

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_and_submit, state=tk.DISABLED, font=("Helvetica", 12))
        self.submit_button.pack(pady=10)

        self.lifeline_button = tk.Button(self.root, text="Use Lifeline", command=self.use_lifeline, state=tk.NORMAL, font=("Helvetica", 12))
        self.lifeline_button.pack(pady=10)

    def start_game(self):
        random.shuffle(self.questions)
        self.show_question()

    def show_question(self):
        if self.current_question < len(self.questions):
            self.timer_seconds = 28
            self.update_timer()
            self.timer_label.set(f'Time Left: {self.timer_seconds} seconds')
            question_data = self.questions[self.current_question]
            self.question_label.config(text=question_data['question'])

            for i, option in enumerate(question_data['options'], 1):
                self.option_buttons[i - 1].config(text=f"{i}. {option}", state=tk.NORMAL, bg='#C0C0C0')  # Change background color

            self.submit_button.config(state=tk.NORMAL)
            self.lifeline_button.config(state=tk.NORMAL)
        else:
            self.show_result()

    def check_and_submit(self, selected_option=None):
        if selected_option is None:
            user_answer = self.user_answer.get()
            if user_answer.isdigit() and 1 <= int(user_answer) <= len(self.questions[self.current_question]['options']):
                selected_option = int(user_answer)
            else:
                messagebox.showerror("Error", "Invalid input. Please enter a valid option.")
                return

        self.attempted_questions += 1
        self.update_attempted_info()

        self.check_answer(selected_option)
        self.current_question += 1
        self.user_answer.set("")  # Clear the entry field
        self.show_question()

    def check_answer(self, user_answer):
        correct_option = self.questions[self.current_question]['answer']
        if user_answer == correct_option:
            self.score += 1
            # Highlight the correct answer
            self.option_buttons[correct_option - 1].config(bg='green')  # Change background color for correct answer
            self.show_popup("Correct!", f"The correct answer is {correct_option}. Well done!")
        else:
            # Highlight the incorrect answer
            self.option_buttons[user_answer - 1].config(bg='red')  # Change background color for incorrect answer
            self.option_buttons[correct_option - 1].config(bg='green')  # Change background color for correct answer
            self.show_popup("Incorrect!", f"The correct answer is {correct_option}. Try again!")

        self.update_attempted_info()

    def show_result(self):
        QuizHistory.save_quiz_result(self.score, len(self.questions))
        result_message = f"Hello {self.participant_name} ({self.participant_age} years old), your final score is: {self.score}/{len(self.questions)}"
        messagebox.showinfo("Game Over", result_message)
        self.root.destroy()

    def update_timer(self):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_label.set(f'Time Left: {self.timer_seconds} seconds')
            self.root.after(1000, self.update_timer)
        else:
            # Disable the Submit button when the timer reaches zero
            self.submit_button.config(state=tk.DISABLED)
            self.lifeline_button.config(state=tk.DISABLED)
            self.show_popup("Time's Up!", "Sorry, time's up! Moving on to the next question.")

    def show_popup(self, title, message):
        popup = tk.Toplevel(self.root)
        popup.title(title)

        label = tk.Label(popup, text=message, font=("Helvetica", 12))
        label.pack(padx=10, pady=10)

        ok_button = tk.Button(popup, text="OK", command=popup.destroy, font=("Helvetica", 12))
        ok_button.pack(pady=10)

    def use_lifeline(self):
        lifeline_options = [lifeline for lifeline, used in self.lifelines_used.items() if not used]
        lifeline = random.choice(lifeline_options)

        if lifeline == "50-50":
            self.use_50_50_lifeline()
        elif lifeline == "Ask the Audience":
            self.use_ask_the_audience_lifeline()

        self.lifelines_used[lifeline] = True
        self.lifeline_button.config(state=tk.DISABLED)

    def use_50_50_lifeline(self):
        question_data = self.questions[self.current_question]
        correct_option = question_data['answer']
        options_to_keep = [correct_option]
        options_to_remove = random.sample(set(range(1, 5)) - set([correct_option]), 2)
        options_to_keep.extend(options_to_remove)

        for i, option in enumerate(question_data['options'], 1):
            if i not in options_to_keep:
                self.option_buttons[i - 1].config(state=tk.DISABLED, text="")

    def use_ask_the_audience_lifeline(self):
        # Simulating audience response (randomly)
        question_data = self.questions[self.current_question]
        correct_option = question_data['answer']
        audience_response = [random.randint(10, 50) for _ in range(4)]
        audience_response[correct_option - 1] += random.randint(20, 30)

        # Normalize audience response percentages
        total_response = sum(audience_response)
        normalized_response = [response / total_response * 100 for response in audience_response]

        # Display audience response in a popup
        response_message = f"Audience Response:\nOption 1: {normalized_response[0]:.2f}%\nOption 2: {normalized_response[1]:.2f}%\nOption 3: {normalized_response[2]:.2f}%\nOption 4: {normalized_response[3]:.2f}%"
        self.show_popup("Ask the Audience", response_message)

    def update_attempted_info(self):
        self.attempted_info_label.config(text=f"Attempted: {self.attempted_questions}")
        self.question_info_label.config(text=f"Questions: {self.current_question + 1}")

if __name__ == "__main__":
    # Sample questions
    questions_data = [
        {
            "question": "Who is known as the 'khiladiyon ka khiladi'?",
            "options": ["Akshay Kumar", "Aamir Khan", "Salman Khan", "Ajay Devgon"],
            "answer": 1,
            "lifeline_tip": "Akshay Kumar is often referred to as the 'khiladiyon ka khiladi' in Bollywood."
        },
        {
            'question': 'Which is the smallest (in area) of the following Union Territories?',
            'options': ['Chandigarh', ' Dadra and Nagar Haveli', 'Daman and Diu', 'Lakshadweep'],
            'answer': 4,
            "lifeline_tip": "Lakshadweep is the smallest Union Territory in terms of area."
        },
        {
            'question': 'What is the largest mammal in the world?',
            'options': ['Elephant', 'Blue Whale', 'Giraffe', 'Hippopotamus'],
            'answer': 2,
            "lifeline_tip": "The Blue Whale is the largest mammal in the world."
        },
        {
             "question": "Which movie is the highest-grossing Bollywood film of all time?",
             "options": ["Dangal", "Baahubali 2: The Conclusion", "PK", "KGF"],
             "answer": 4,
             "lifeline_tip": "KGF is one of the highest-grossing Bollywood films of all time."
        },
    ]

    entry_page = ParticipantDetailsPage(tk.Tk(), lambda: QuizGame(questions_data))
    entry_page.master.mainloop()
