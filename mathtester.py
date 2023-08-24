import tkinter as tk
import random
from os import system as sys
import tkinter.font as tkFont
import webbrowser

root = tk.Tk()
root.title("MathTester v11.81b")
root.geometry("1300x600")
root.wm_minsize(1300, 600)

score = 0
time_limit = random.randint(3, 90) * 60  # Update time_limit to a random value between 3 and 90 minutes
st_time_limit = time_limit
total_tasks = 1
correct_tasks = 0
timer_id = None  # Initialize the timer_id variable
foil = 0
hints = 3


#Прикрутить к гитхабу, чтобы через него обновлять новости.
informational_panel_text = r'''
Last update:// 8/24/2023 11:02pm

 MathTester is a generator of mathematical examples 
 for learning and repeating and consolidating 
 the acquired knowledge.

----------------------------------------------------

Правила:

1. Вводите ответ с округлением до сотых долей.
   например: Вы получили ответ: 7.135, 
   в поле ввода ответов вводим: 7.14 

   Если вы получили целый ответ, то вводите его 
   как есть, например число 89, в поле ответов,
   мы введём ровно так же как и получили: 89

2. Если задача, которую вы решаете, слишком сложная,
   то чтобы не тратить на неё время вы можете
   использовать комманду: skip,
   дабы пропустить её и узнать ответ.

----------------------------------------------------

            Разработчик: Назарян A.K                '''

def open_link(event):
    webbrowser.open("https://t.me/Slide36")

def theme():  #выбор тем. (Тёмная и светлая)
    pass


def generate_task():
    global numbers, operators, result
    
    num_count = random.randint(2, 5)
    numbers = [random.randint(-64, 256) for _ in range(num_count)]

    if total_tasks <= 5:
        operators = [random.choice(["+", "-"]) for _ in range(num_count-1)]
    elif total_tasks <=14:
        operators = [random.choice(["+", "-", "*", "/"]) for _ in range(num_count-1)]
    elif total_tasks >=15:
        operators = [random.choice(["+", "-", "*", "/", "**"]) for _ in range(num_count-1)]

    expr = ""
    expr_print = ""

    for i in range(num_count-1):
        operator = operators[i]
        
        if operator == '/':
            operator = ':'
        elif operator == '**':
            operator = '^'
        
        expr += f"({numbers[i]} {operators[i]} "
        expr_print += f"({numbers[i]} {operator} "
    
    expr += f"{numbers[-1]}" + ")" * (num_count-1)
    expr_print += f"{numbers[-1]}" + ")" * (num_count-1)
    
    try:
        result = round(eval(expr), 2)
        
        if operators.count('**') > 0 and (result > 256000 and result < -256000 and (max(numbers) > 8 and min(numbers) > -8)):
            print('Ответ или число в степени превышает стандарт, повторная генерация!')
            generate_task()  # Выбираем другие числа
            return
        
        print(result)
        
    except ZeroDivisionError:
        generate_task()
        return
    
    numbers_str = " ".join(str(num) for num in numbers)
    task_label.config(text=f"Текущий пример #{total_tasks}\n\n{expr_print} =")

def check_answer():
    global time_limit, total_tasks,score, correct_tasks, foil,hints,score,total_tasks,correct_tasks, foil,hints,stats_frame
    try:
        user_answer = (user_entry.get())
        if user_answer == 'skip':
            answer_label.config(text="\nПропущено!\nОтвет: " + str(result), fg='red', font=('consolas', 12))
        else:
            user_answer = float(user_answer)

            if user_answer == result:
                score += 1
                hints += 0.5
                time_limit = max(time_limit+10, 90*60)  # Update the maximum time_limit value to 90 minutes
                correct_tasks += 1
                total_tasks += 1
                score_label.config(text="Score: " + str(score))
                result_text = f"\nCorrect!\n"
                hint_button.configure(text=f"Hint: {hints}")
                answer_label.config(text=result_text, fg='green', font=('consolas', 12))

            else:
                result_text = f"Incorrect!\nYour answer: {user_answer}\nCorrect answer: {result}"
                total_tasks += 1
                hint_button.configure(text=f"Hint: {hints}")
                answer_label.config(text=result_text, fg='red', font=('consolas', 12))
        user_entry.delete(0, tk.END)
        generate_task()
    except ValueError:
        result_text = '\nThe received response is not supported!\n'
        answer_label.config(text=result_text, fg='red', font=('consolas', 12))

        user_entry.delete(0, tk.END)

def hint():
    global score,hints
    if score > 0 and hints > 0.9:
        score -= 1
        hints -= 1
        score_label.config(text="Score: " + str(score))
        hint_button.configure(text=f"Hint: {hints}")
        answer_label.config(text=result)

def update_timer(time_limit):
    timer_label.config(text="Time left: " + str(time_limit) + "s")
    
    if time_limit <= 0:
        global score,total_tasks,correct_tasks, foil,hints,stats_frame
        #root.after_cancel(timer_id)
        
        if correct_tasks == 0 and total_tasks == 0 or 1:
            foil = 2
        if correct_tasks > total_tasks:
            foil = 2
        else:
            foil = round(5*(correct_tasks/total_tasks), 2)
            if foil <= 2:
                foil = 2
            elif foil >=5:
                foil = 5
        

        user_entry.config(state="disabled")
        hint_button.config(state="disabled")
        task_frame.pack_forget()
        result_frame.pack_forget()
        stats_frame = tk.Frame(root, bg="white")
        stats_frame.pack(padx=20, pady=20)

        if total_tasks > 1: #Убираем заданее, которое может появится на последней секунде ("Оценка в пользу ученика")
            total_tasks -= 1

        stats_label = tk.Label(stats_frame, text=f"Вы решили {total_tasks} задач за {st_time_limit} секунд! \n{correct_tasks} из них были правильными.\n\nОценка: {foil}", font=("consolas", 24), bg="white")
        stats_label.pack()
        restart_button = tk.Button(stats_frame, text="Restart?", font=("consolas", 16), command=restart_test, width=20, relief='ridge',activebackground='white',background='white')
        restart_button.pack(pady=10)
        menu_button = tk.Button(stats_frame, text="back to menu", font=("consolas", 16), command=mainmenu, width=20, relief='groove',activebackground='white',background='white')
        menu_button.pack(pady=10)
    else:
        time_limit -= 1
        timer_id = root.after(1000, update_timer, time_limit)  # Initialize timer_id here

def restart_test():
    global score, time_limit, total_tasks, correct_tasks, timer_id,hints,tester,st_time_limit  # Add timer_id here
    score = 0
    time_limit = random.randint(3, 90) * 60  # Update time_limit to a random value between 3 and 90 minutes
    total_tasks = 1
    st_time_limit = time_limit
    correct_tasks = 0
    hints = 3
    generate_task()
    update_timer(time_limit)
    user_entry.config(state="normal")
    hint_button.config(state="normal")
    stats_frame.pack_forget()
    task_frame.pack_forget()
    result_frame.pack_forget()
    tester()

def StartButton_():
        global MainLogo,StartButton,SettingsButton,feedback_button, informational_panel,feedback_btn,site_label
        print("command started")

        MainLogo.place_forget()
        StartButton.place_forget()
        informational_panel.place_forget()
        site_label.place_forget()
        #SettingsButton.place_forget()
        feedback_btn.place_forget()

        tester()

def SettingsButton_():
        print("command settings")

def open_site(event):
    webbrowser.open("https://github.com/SL1dee36?tab=repositories")

def mainmenu():
    global MainLogo,StartButton,SettingsButton,feedback_button, informational_panel,feedback_btn,site_label

    try:
        stats_frame.pack_forget()
    except:
        pass

    MainLogo=tk.Label(root, bg="white", font=("Consolas", 32),width=80, justify="center", text='MathTester:Betas')
    MainLogo.place(x=30,y=30,width=400,height=60)

    StartButton=tk.Button(root,text='Начать тестирование',bg='#393d49',fg='white',font=('cornier', 16), justify="center", relief='solid',command=StartButton_,cursor="hand2")
    StartButton.place(x=80,y=280,width=300,height=75)

    informational_panel=tk.Text(root, height=16, width=45, font=("consolas", 11), relief='solid')
    informational_panel.place(x=690,y=30,width=470,height=530)
    informational_panel.insert(tk.END, informational_panel_text)
    informational_panel.config(state="disabled")

    site_text = 'Больше программ тут: GITHUB'

    site_label=tk.Label(root,text=f'{site_text}', bg='white', font=('cornier', 12), justify='left', relief='flat', fg="#0064ff",cursor="hand2")
    site_label.place(x=80,y=500,width=300,height=50)
    site_label.bind("<Button-1>", open_site)

    feedback_btn = tk.Label(root, text="feedback", fg="#0064ff", cursor="hand2", width=13, font=("cornier", 12),bg='white')
    feedback_btn.place(x=80,y=460,width=300,height=50)
    feedback_btn.bind("<Button-1>", open_link)

    root.configure(bg="white")
    root.mainloop()

def tester():
    global stats_frame,user_entry,hint_button,task_frame,total_tasks,correct_tasks,result_frame,score_label,timer_label,task_label,answer_label,correct_label,feedback_btn,site_label
    
    try:
        MainLogo.place_forget()
        StartButton.place_forget()
        informational_panel.place_forget()
        site_label.place_forget()
        #SettingsButton.place_forget()
        feedback_btn.place_forget()
    except:
        pass

    try:
        stats_frame.pack_forget()
    except:
        pass


    task_frame = tk.Frame(root, bg="white")
    task_frame.pack(side="left", padx=20, pady=20)

    result_frame = tk.Frame(root, bg="white")
    result_frame.pack(side="right", padx=20, pady=20)


    task_label = tk.Label(task_frame, text="", font=("consolas", 24), bg="white")
    task_label.pack(padx=50)

    user_entry = tk.Entry(task_frame, font=("consolas", 24), width=32, justify='center', relief='solid')
    user_entry.pack()

    check_button = tk.Button(task_frame, text="Send answer", font=("consolas", 16), command=check_answer, width=15, relief='groove',activebackground='white',background='white')
    check_button.pack(pady=10, padx=50)

    score_label = tk.Label(result_frame, text="Score: 0", font=("consolas", 24), bg="white")
    score_label.pack(pady=10)

    timer_label = tk.Label(result_frame, text="Time left: " + str(time_limit) + "s", font=("consolas", 20), bg="white")
    timer_label.pack(padx=50)

    answer_label = tk.Label(result_frame, text="", font=("consolas", 20), bg="white")
    answer_label.pack(padx=50)


    hint_button = tk.Button(result_frame, text=f"Hint: {hints}", font=("consolas", 16), command=hint, width=15, relief='flat',activebackground='white',background='white')
    hint_button.pack(pady=10, padx=50)

    generate_task()
    update_timer(time_limit)

    root.configure(bg="white")
    task_frame.configure(bg="white")
    result_frame.configure(bg="white")

    root.mainloop()

mainmenu()
