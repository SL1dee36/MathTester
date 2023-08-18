import tkinter as tk
import random
import math
from math import cos,sin,tan,sqrt,sqrt,pi

root = tk.Tk()
root.title("MathTester v9.11b")
root.geometry("1200x600")
root.wm_minsize(1200, 600)

score = 0
time_limit = 7 * 60  # 3 minutes
st_time_limit = time_limit
total_tasks = 0
correct_tasks = 0
timer_id = None  # Initialize the timer_id variable
foil = 0

def generate_task():
    global numbers, operators, result
    
    num_count = random.randint(2, 5)
    numbers = [random.randint(-99, 99) for _ in range(num_count)]
    operators = [random.choice(["+", "-", "*", "/"]) for _ in range(num_count-1)] #add !,^,sqrt,log,sin(),cos() & more features
    
    expr = ""
    for i in range(num_count-1):
        expr += f"({numbers[i]} {operators[i]} "
    expr += f"{numbers[-1]}" + ")" * (num_count-1)
    
    try:
        result = round(eval(expr),2)
    except ZeroDivisionError:
        generate_task()
        return
    
    numbers_str = " ".join(str(num) for num in numbers)
    task_label.config(text=f"{expr} =")

def check_answer():
    global time_limit, total_tasks,score, correct_tasks, foil
    user_answer = float(user_entry.get())


    if user_answer == result:
        score += 1
        time_limit = time_limit+10
        correct_tasks += 1
        total_tasks += 1
        score_label.config(text="Score: " + str(score))
        result_text = f"Correct!\n\n"
        answer_label.config(text=result_text, fg='green')

        foil = round(5*(correct_tasks/total_tasks), 2)
    else:
        result_text = f"Incorrect!\nYour answer: {user_answer}\nCorrect answer: {result}"
        total_tasks += 1
        answer_label.config(text=result_text, fg='red')
    
    user_entry.delete(0, tk.END)
    generate_task()

def hint():
    global score
    if score > 0:
        score -= 1
        score_label.config(text="Score: " + str(score))
        answer_label.config(text=result)

def update_timer(time_limit):
    timer_label.config(text="Time left: " + str(time_limit) + "s")
    
    if time_limit <= 0:
        global score,total_tasks,correct_tasks, foil
        #root.after_cancel(timer_id)
        user_entry.config(state="disabled")
        hint_button.config(state="disabled")
        task_frame.pack_forget()
        result_frame.pack_forget()
        stats_frame = tk.Frame(root, bg="white")
        stats_frame.pack(padx=20, pady=20)
        stats_label = tk.Label(stats_frame, text=f"You solved {total_tasks} tasks in {st_time_limit} seconds! \n{correct_tasks} of them were correct.\n\nОценка: {foil}", font=("consolas", 24), bg="white")
        stats_label.pack()
        restart_button = tk.Button(stats_frame, text="Restart?", font=("consolas", 16), command=restart_test, width=15, relief='flat')
        restart_button.pack(pady=10)
    else:
        time_limit -= 1
        timer_id = root.after(1000, update_timer, time_limit)  # Initialize timer_id here

def restart_test():
    global score, time_limit, total_tasks, correct_tasks, timer_id  # Add timer_id here
    score = 0
    time_limit = 7 * 60
    total_tasks = 0
    correct_tasks = 0
    generate_task()
    update_timer(time_limit)
    user_entry.config(state="normal")
    hint_button.config(state="normal")
    task_frame.pack_forget()
    result_frame.pack_forget()

task_frame = tk.Frame(root, bg="white")
task_frame.pack(side="left", padx=20, pady=20)

result_frame = tk.Frame(root, bg="white")
result_frame.pack(side="right", padx=20, pady=20)

task_label = tk.Label(task_frame, text="", font=("consolas", 24), bg="white")
task_label.pack(padx=50)

user_entry = tk.Entry(task_frame, font=("consolas", 24), width=32, justify='center')
user_entry.pack()

check_button = tk.Button(task_frame, text="Send answer", font=("consolas", 16), command=check_answer, width=10, relief='flat')
check_button.pack(pady=10, padx=50)

score_label = tk.Label(result_frame, text="Score: 0", font=("consolas", 24), bg="white")
score_label.pack(pady=10)

timer_label = tk.Label(result_frame, text="Time left: " + str(time_limit) + "s", font=("consolas", 20), bg="white")
timer_label.pack(padx=50)

answer_label = tk.Label(result_frame, text="", font=("consolas", 20), bg="white")
answer_label.pack(padx=50)

hint_button = tk.Button(result_frame, text="Hint", font=("consolas", 16), command=hint, width=10, relief='flat')
hint_button.pack(pady=10, padx=50)

generate_task()
update_timer(time_limit)

root.configure(bg="white")
task_frame.configure(bg="white")
result_frame.configure(bg="white")

root.mainloop()