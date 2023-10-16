import easygui
import keyboard
import pyautogui
import time
import threading
from ttkbootstrap import *
from tkinter import filedialog
import os

pyautogui.PAUSE = 0 #Set up a 2.5 second pause after each PyAutoGUI call:
#pyautogui.FAILSAFE = False

root = tk.Tk()
style = Style(theme="minty")
root.columnconfigure(0, minsize=210)

# globalne varijable
i = 0
k = 0
l = 0
m = 0
n = 0
rowNum = 5
columnNum = 0
tasksStarted = False
actionList = []
chosenTasksList = []
entryXList = []
entryYList = []
entryRepeatList = []
taskDelayList = []
entryXListVar = []
entryYListVar = []
entryRepeatListVar = []
entryDelayListVar = []
options = {
    0:"(choose)",
    1:"MOVE MOUSE TO",
    2:"MOVE TO AND CLICK",
    3:"RIGHT CLICK",
    4:"LEFT CLICK",
    5:"SCROLL UP",
    6:"SCROLL DOWN",
    7:"MIDDLE CLICK",
    8:"WAIT(s)",
    9:"RELATIVE MOVE TO",
    10:"DRAG MOUSE TO",
    11:"RELAT MOUSE DRAG",
    12:"TEXT INPUT",
    13:"COPY SELECTED",
    14:"PASTE",
    15:"CUT"
}


# funkcije

def create_file():
    global i


    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    try:
        with open(file_path, "w") as file:


            ponavljanje = ponavljanjeSekvenceEntry.get() if ponavljanjeSekvenceEntry.get() != "" else "1"

            wait = entryWaitBeforeStart.get() if entryWaitBeforeStart.get() != "" else "0.1"

            file.write(ponavljanje + " " + wait + "\n")

            for x in range(i):

                taskOption = find_key_by_value(options,chosenTasksList[x].get())

                entryXText = entryXList[x].get()
                entryX = entryXText if len(entryXText)>0 else '.'

                entryYText = entryYList[x].get()
                entryY = entryYText if len(entryYText) > 0 else '.'

                entryRepeatText = entryRepeatList[x].get()
                entryRepeat = entryRepeatText if len(entryRepeatText) > 0 else '.'

                taskDelayText = taskDelayList[x].get()
                taskDelay = taskDelayText if len(taskDelayText) > 0 else '.'

                newLine = "\n" if x != i-1 else ""


                if int(taskOption) == 12:
                    file.write(taskOption + " " + entryY + " " + entryRepeat + " " + taskDelay + "\n")
                    file.write(entryX + newLine)
                else:
                    file.write(taskOption + " " + entryX + " " + entryY + " " + entryRepeat + " " + taskDelay + newLine)

    except FileNotFoundError:
        return
    os.chmod(file_path, 0o444)

def find_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return str(key)

def load_file():
    global i
    j=0
    line_count = -1
    skipLine = False
    firstLine = True
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

    try:
        with open(file_path, "r") as file:
            for line in file:
                line_count += 1
    except FileNotFoundError:
        return

    for x in range(i):
        remove_task()



    with open(file_path, "r") as file:
        for line in file:

            if firstLine:
                lineNiz1 = line.split()
                ponavljanjeSekvenceEntry.delete(0, END)
                entryWaitBeforeStart.delete(0, END)
                ponavljanjeSekvenceEntry.insert(0, lineNiz1[0])
                entryWaitBeforeStart.insert(0, lineNiz1[1])
                firstLine = False
                continue

            if skipLine:
                skipLine=False
                entryXList[j-1].insert(0, line)
                continue

            lineNiz = line.split()

            if int(lineNiz[0]) == 12:
                chosenTasksList[j].set("TEXT INPUT")
                skipLine=True
                line_count-=1
                taskDelayList[j].delete(0, END)
                taskDelayList[j].insert(0, lineNiz[3])
            else:
                chosenTasksList[j].set(options.get(int(lineNiz[0]),"You like to snoop around, don't ya? :)"))
                entryXList[j].insert(0, lineNiz[1])
                entryYList[j].insert(0, lineNiz[2])
                entryRepeatList[j].delete(0, END)
                entryRepeatList[j].insert(0, lineNiz[3])
                taskDelayList[j].delete(0, END)
                taskDelayList[j].insert(0, lineNiz[4])


            j += 1

            addTask() if j != line_count else ''
def addTask():
    global columnNum, rowNum, i

    chosenTask = StringVar()

    action = OptionMenu(root, chosenTask, "", "MOVE MOUSE TO", "MOVE TO AND CLICK", "RIGHT CLICK", "LEFT CLICK", "SCROLL UP", "SCROLL DOWN", "MIDDLE CLICK", "WAIT(s)","RELATIVE MOVE TO","DRAG MOUSE TO","RELAT MOUSE DRAG","TEXT INPUT","COPY SELECTED","PASTE","CUT")
    action.grid(row=rowNum, column=columnNum,pady=5,padx=1)
    actionList.append(action)

    chosenTask.set("(choose)")
    chosenTask.trace_add('write', lambda *args, index=i: chosenTaskChange(index, *args))
    chosenTasksList.append(chosenTask)

    entry_varX = StringVar()
    columnNum += 1
    entryX = tk.Entry(root,bd=5,textvariable=entry_varX)
    entryX.grid(row=rowNum, column=columnNum,padx=1)
    entryXList.append(entryX)
    entryXListVar.append(entry_varX)
    entryXListVar[i].trace_add("write",lambda *args, index=i:value_changed_pos_int_entryX(index))

    entry_varY = StringVar()
    columnNum += 1
    entryY = tk.Entry(root,bd=5,textvariable=entry_varY)
    entryY.grid(row=rowNum, column=columnNum,padx=1)
    entryYList.append(entryY)
    entryYListVar.append(entry_varY)
    entryYListVar[i].trace_add("write", lambda *args, index=i: value_changed_pos_int_entryY(index))

    entry_var_Repeat = StringVar()
    columnNum += 1
    entryRepeat = tk.Entry(root,bd=5, textvariable=entry_var_Repeat)
    entryRepeat.grid(row=rowNum, column=columnNum,padx=1)
    entryRepeatList.append(entryRepeat)
    entryRepeatListVar.append(entry_var_Repeat)
    entryRepeatListVar[i].trace_add("write", lambda *args, index=i:value_changed_pos_int_Repeat(index))

    entry_var_RepeatDelay = StringVar()
    columnNum += 1
    taskDelay = tk.Entry(root,bd=5,textvariable=entry_var_RepeatDelay)
    taskDelay.grid(row=rowNum, column=columnNum)
    taskDelayList.append(taskDelay)
    entryDelayListVar.append(entry_var_RepeatDelay)
    entryDelayListVar[i].trace_add("write", lambda *args, index=i: value_changed_pos_float_RepeatDelay(index))

    columnNum = 0

    entryXList[i].configure(state=DISABLED)
    entryYList[i].configure(state=DISABLED)
    entryRepeatList[i].configure(state=DISABLED)
    taskDelayList[i].configure(state=DISABLED)


    rowNum += 1
    i += 1
    return


def remove_task():
    global i

    i -= 1
    actionList[i].destroy()
    entryXList[i].destroy()
    entryYList[i].destroy()
    entryRepeatList[i].destroy()
    taskDelayList[i].destroy()

    actionList.pop()
    chosenTasksList.pop()
    entryXList.pop()
    entryYList.pop()
    entryRepeatList.pop()
    taskDelayList.pop()
    entryDelayListVar.pop()
    entryRepeatListVar.pop()
    entryXListVar.pop()
    entryYListVar.pop()



    if i==0:
        addTask()

def chosenTaskChange(index, *args):
    selected_task = chosenTasksList[index].get()
    entryXList[index].configure(state=NORMAL)
    entryYList[index].configure(state=NORMAL)
    entryRepeatList[index].configure(state=NORMAL)
    taskDelayList[index].configure(state=NORMAL)
    entryXList[index].delete(0, END)
    entryYList[index].delete(0, END)
    entryRepeatList[index].delete(0,END)
    taskDelayList[index].delete(0,END)
    entryRepeatList[index].insert(0,"1")
    taskDelayList[index].insert(0,"0.1")



    if selected_task == "LEFT CLICK" or selected_task == "RIGHT CLICK" or selected_task == "MIDDLE CLICK" or selected_task == "COPY SELECTED" or selected_task == "PASTE" or selected_task == "CUT":
        entryXList[index].delete(0, END)
        entryYList[index].delete(0, END)
        entryXList[index].configure(state=DISABLED)
        entryYList[index].configure(state=DISABLED)
    elif selected_task == "WAIT(s)" or selected_task == "SCROLL UP" or selected_task == "SCROLL DOWN":
        entryYList[index].delete(0, END)
        entryYList[index].configure(state=DISABLED)
    elif selected_task == "RELAT MOUSE DRAG" or selected_task == "DRAG MOUSE TO":
        entryRepeatList[index].delete(0, END)
        entryRepeatList[index].configure(state=DISABLED)
    elif selected_task == "TEXT INPUT":
        entryRepeatList[index].delete(0, END)
        entryRepeatList[index].configure(state=DISABLED)
        entryYList[index].delete(0, END)
        entryYList[index].configure(state=DISABLED)
    elif selected_task == "(choose)":
        entryXList[index].delete(0, END)
        entryYList[index].delete(0, END)
        entryXList[index].configure(state=DISABLED)
        entryYList[index].configure(state=DISABLED)
        entryRepeatList[index].delete(0, END)
        entryRepeatList[index].configure(state=DISABLED)
        taskDelayList[index].delete(0, END)
        taskDelayList[index].configure(state=DISABLED)


def move(x,y):
    pyautogui.moveTo(x, y)

def copy():
    pyautogui.hotkey('ctrl', 'c')

def paste():
    pyautogui.hotkey('ctrl', 'v')

def cut():
    pyautogui.hotkey('ctrl', 'x')

def leftClick():
    pyautogui.click()

def rightClick():
    pyautogui.rightClick()

def sleep(x):
    if x<0:
        return
    time.sleep(x)

def moveRel(x,y):
    pyautogui.move(x, y)

def dragTo(x,y,z):
    pyautogui.dragTo(x, y,z, button='left')

def dragRel(x,y,z):
    pyautogui.drag(x,y, z, button='left')

def middleClick():
    pyautogui.click(button='middle')

def moveAndClick(x,y):
    pyautogui.click(x=x, y=y)

def scrollUp(x):
    pyautogui.scroll(x)

def scrollDown(x):
    pyautogui.scroll(-1*x)

def textInput(str,interval):
    if interval < 0.01:
        interval = 0.01
    try:
        pyautogui.write(str,interval=interval)
    except:
        return


def start_tasks():
    try:
        root.withdraw()

        try:
            sleep(float(entryWaitBeforeStart.get()))
        except:
            entryWaitBeforeStart.delete(0, "end")
            entryWaitBeforeStart.insert(0,"0")

        global i, k, l, m, n, tasksStarted

        try:
            n = int(ponavljanjeSekvenceEntry.get())
        except:
            ponavljanjeSekvenceEntry.delete(0, "end")
            ponavljanjeSekvenceEntry.insert(0,"1")

        tasksStarted = True
        # ponavljanje sekvence n puta
        m = 0
        for m in range(n):
            # prolazak kroz 'i' broja zadataka
            j = 0
            for j in range(i):
                try:
                    l = int(entryRepeatList[j].get())
                except:
                    entryRepeatList[j].insert(0,"1")
                    l = 1

                # ponavljanje jednog zadatka l puta
                k = 0
                taks = chosenTasksList[j].get()

                try:
                    delay = float(taskDelayList[j].get())
                except:
                    taskDelayList[j].insert(0,"0.1")
                    delay = 0

                if entryXList[j].get() == "":
                    entryXValue = 0
                else:
                    entryXValue = entryXList[j].get()

                if entryYList[j].get() == "":
                    entryYValue = 0
                else:
                    entryYValue = entryYList[j].get()

                if taks == "LEFT CLICK":
                    for k in range(l):
                        leftClick()
                        sleep(delay)
                elif taks == "TEXT INPUT":
                    for k in range(l):
                        textInput(str(entryXValue),delay)
                elif taks == "RIGHT CLICK":
                    for k in range(l):
                        rightClick()
                        sleep(delay)
                elif taks == "MOVE TO AND CLICK":
                    for k in range(l):
                        moveAndClick(int(entryXValue),int(entryYValue))
                        sleep(delay)
                elif taks == "WAIT(s)":
                    for k in range(l):
                        sleep(float(entryXValue))
                        sleep(delay)
                elif taks == "MOVE MOUSE TO":
                    for k in range(l):
                        move(int(entryXValue), int(entryYValue))
                        sleep(delay)
                elif taks == "MIDDLE CLICK":
                    for k in range(l):
                        middleClick()
                        sleep(delay)
                elif taks == "RELATIVE MOVE TO":
                    for k in range(l):
                        moveRel(int(entryXValue),int(entryYValue))
                        sleep(delay)
                elif taks == "DRAG MOUSE TO":
                    for k in range(l):
                        dragTo(int(entryXValue),int(entryYValue),delay)
                        sleep(delay)
                elif taks == "RELAT MOUSE DRAG":
                    for k in range(l):
                        dragRel(int(entryXValue),int(entryYValue),delay)
                        sleep(delay)
                elif taks == "SCROLL UP":
                    for k in range(l):
                        scrollUp(int(entryXValue))
                        sleep(delay)
                elif taks == "SCROLL DOWN":
                    for k in range(l):
                        scrollDown(int(entryXValue))
                        sleep(delay)
                elif taks == "COPY SELECTED":
                    for k in range(l):
                        copy()
                        sleep(delay)
                elif taks == "PASTE":
                    for k in range(l):
                        paste()
                        sleep(delay)
                elif taks == "CUT":
                    for k in range(l):
                        cut()
                        sleep(delay)
        root.deiconify()
        tasksStarted = False
        startFindPos()
    except pyautogui.FailSafeException:
        root.deiconify()
        startFindPos()
        tasksStarted = False


def value_changed_pos_int_Repeat(i):
    value = entryRepeatList[i].get()
    if len(value)==0:
        return
    if value[-1].isnumeric():
        return
    else:
        new_value = value[:-1]
        entryRepeatList[i].delete(0, "end")
        entryRepeatList[i].insert(0, new_value)


def value_changed_pos_float_RepeatDelay(index):
    value = taskDelayList[index].get()

    if len(value) == 0:
        return
    if value[0] == ".":
        new_value = value[:-1]
        taskDelayList[index].delete(0, "end")
        taskDelayList[index].insert(0, new_value)
    if value[-1].isnumeric() or value[-1] == ".":
        if value.count(".") == 2:
            new_value = value[:-1]
            taskDelayList[index].delete(0, "end")
            taskDelayList[index].insert(0, new_value)
        return

    else:
        new_value = value[:-1]
        taskDelayList[index].delete(0, "end")
        taskDelayList[index].insert(0, new_value)

def value_changed_pos_int_ponavljanjeSekvenceEntry():

    value = ponavljanjeSekvenceEntry.get()
    if len(value)==0:
        return
    if value[-1].isnumeric():
        return
    else:
        new_value = value[:-1]
        ponavljanjeSekvenceEntry.delete(0, "end")
        ponavljanjeSekvenceEntry.insert(0, new_value)

def value_changed_pos_int_entryX(index):
    value = entryXList[index].get()
    option_val = chosenTasksList[index].get()
    valid_options = ["MOVE MOUSE TO","SCROLL UP","SCROLL DOWN","DRAG MOUSE TO","MOVE TO AND CLICK"]

    if option_val not in valid_options:
        if option_val == "WAIT(s)":
            value_changed_pos_float_WAIT(index)
        if option_val == "RELATIVE MOVE TO" or option_val == "RELAT MOUSE DRAG":
            value_changed_neg_int_RELATIVEX(index)
        return
    if len(value)==0:
        return
    if value[-1].isnumeric():
        return
    else:
        new_value = value[:-1]
        entryXList[index].delete(0, "end")
        entryXList[index].insert(0, new_value)

def value_changed_neg_int_RELATIVEX(index):
    value = entryXList[index].get()

    if len(value)==0:
        return
    if value[-1].isnumeric():
        return
    if len(value) == 1 and value[0] == "-":
        return
    else:
        new_value = value[:-1]
        entryXList[index].delete(0, "end")
        entryXList[index].insert(0, new_value)

    return


def value_changed_neg_int_RELATIVEY(index):
    value = entryYList[index].get()

    if len(value) == 0:
        return
    if value[-1].isnumeric():
        return
    if len(value) == 1 and value[0] == "-":
        return
    else:
        new_value = value[:-1]
        entryYList[index].delete(0, "end")
        entryYList[index].insert(0, new_value)

    return

def value_changed_pos_int_entryY(index):
    value = entryYList[index].get()
    option_val = chosenTasksList[index].get()
    valid_options = ["MOVE MOUSE TO","SCROLL UP","SCROLL DOWN","DRAG MOUSE TO","MOVE TO AND CLICK"]

    if option_val not in valid_options:
        if option_val == "RELATIVE MOVE TO" or option_val == "RELAT MOUSE DRAG":
            value_changed_neg_int_RELATIVEY(index)
        return
    if len(value)==0:
        return
    if value[-1].isnumeric():
        return
    else:
        new_value = value[:-1]
        entryYList[index].delete(0, "end")
        entryYList[index].insert(0, new_value)


def value_changed_pos_float_WAIT(index):
    value = entryXList[index].get()
    option_val = chosenTasksList[index].get()

    if len(value) == 0:
        return
    if value[0] == ".":
        entryXList[index].delete(0, "end")
        return
    if value[-1].isnumeric() or value[-1] == ".":
            if value.count(".") == 2:
                new_value = value[:-1]
                entryXList[index].delete(0, "end")
                entryXList[index].insert(0, new_value)
            return
    else:
        new_value = value[:-1]
        entryXList[index].delete(0, "end")
        entryXList[index].insert(0, new_value)

def value_changed_pos_float_WaitBeforeStart():
    value = entryWaitBeforeStart.get()

    if len(value) == 0:
        return
    if value[0] == ".":
        new_value = value[:-1]
        entryWaitBeforeStart.delete(0, "end")
        entryWaitBeforeStart.insert(0, new_value)
    if value[-1].isnumeric() or value[-1] == ".":
        if value.count(".") == 2:
            new_value = value[:-1]
            entryWaitBeforeStart.delete(0, "end")
            entryWaitBeforeStart.insert(0, new_value)
        return
    else:
        new_value = value[:-1]
        entryWaitBeforeStart.delete(0, "end")
        entryWaitBeforeStart.insert(0, new_value)

def deleteAll(timeHeld):
    if timeHeld >= 1:
        for x in range(i):
            remove_task()
    else:
        remove_task()


def start_deleting(args):
    global start_time
    start_time = time.time()


def stop_deleting(args):
    global end_time
    end_time = time.time()

    timeHeld = end_time - start_time

    deleteAll(timeHeld)


# pravljenje staticne grafike

separator1 = ttk.Separator(root, orient="horizontal")
separator1.grid(row=1, column=0, columnspan=5, sticky="ew", pady=10)

separator2 = ttk.Separator(root, orient="horizontal")
separator2.grid(row=3, column=0, columnspan=5, sticky="ew", pady=10)

root.title("Untangle")
root.geometry("920x600")

entry_var_ponavaljanjeSekvence = StringVar()
ponavljanjeSekvenceEntry = Entry(root,textvariable=entry_var_ponavaljanjeSekvence)
ponavljanjeSekvenceEntry.insert(0, "1")
ponavljanjeSekvenceEntry.grid(row=2, column=1)
entry_var_ponavaljanjeSekvence.trace_add("write",lambda *args:value_changed_pos_int_ponavljanjeSekvenceEntry())

entry_var_WaitBeforeStart = StringVar()
entryWaitBeforeStart = Entry(root,textvariable=entry_var_WaitBeforeStart)
entryWaitBeforeStart.insert(0,"0")
entryWaitBeforeStart.grid(row=2,column=3)
entry_var_WaitBeforeStart.trace_add("write",lambda *args:value_changed_pos_float_WaitBeforeStart())



labelSekvence = Label(root, text="Repeat sequence times:")
labelSekvence.grid(row=2, column=0)

labelWaitBeforeStart = Label(root, text="Wait (s) before start:")
labelWaitBeforeStart.grid(row=2,column=2)

labelTask = Label(root, text="Task Action")
labelTask.grid(row=4, column=0)

labelX = Label(root, text="X Coordinate/Value/(s)")
labelX.grid(row=4, column=1)

labelY = Label(root, text="         Y Coordinate", width=20)
labelY.grid(row=4, column=2)

labelRepeat = Label(root, text="     Repeat task times", width=20)
labelRepeat.grid(row=4, column=3)

labelDelay = Label(root, text="Wait btwn repetitions(s)", width=20)
labelDelay.grid(row=4, column=4)

dodajTaskBtn = Button(root, text="Add Task", command=addTask)
dodajTaskBtn.grid(row=0, column=0)

obrisiTaskBtn = Button(root, text="Delete Task",style='secondary.TButton')
obrisiTaskBtn.grid(row=0, column=1)
obrisiTaskBtn.bind("<ButtonPress-1>", start_deleting)
obrisiTaskBtn.bind("<ButtonRelease-1>", stop_deleting)




startTaskBtn = Button(root, text="Start Tasks", style='success.TButton' ,command=lambda: threading.Thread(target=start_tasks).start())
startTaskBtn.grid(row=0, column=2)

saveSeqBtn = Button(root, text="Save Sequence", style='info.outline' ,command=create_file)
saveSeqBtn.grid(row=0, column=3)

loadSeqBtn = Button(root, text="Load Sequence", style='info.outline' ,command=load_file)
loadSeqBtn.grid(row=0, column=4)

tooltipsBtn = Button(root, text="Tooltips/Help",style='warning.TButton', command=lambda: easygui.msgbox("Help and Tips for using Untangle:\n\n1) To stop sequence executing put mouse to any corner of the sceen and wait a bit until window shows again.\n2) Press F11 to get current position of your mouse and save it to latest task coordinates.\n3) All wait/delay times are in seconds(s).\n4)'Relative' moves mouse x or y amount relative to current mouse position. Example: value of 100 in X Axis moves mouse right 100 pixels, -100 moves to the left.\n5) Most of value entries accept only whole numbers, some accept negative or rational.\n6) Drag options clicks and holds mouse until the end of the drag. Delay value is how fast the drag is.\n7) Text input task can take up to 6000 characters.\n8) Delay in text input task changes how fast characters are inputted. 0.1 delay means every character is inputted after 1 10th of a second (That is the fastest input speed).\n9) Holding Delete Task button for 1 second deletes all tasks.\n\n\n\nMade by:\nJanko Veselinovic 2023", title="How to use"))
tooltipsBtn.grid(row=2,column=4)

style.configure('TButton', font=('Helvetica', 11), borderwidth=6)

#style='light.outline' for hidden button for easter egg

def getPosition():
    global X, Y
    X, Y = pyautogui.position()

    entryXList[i-1].delete(0, END)
    entryYList[i-1].delete(0, END)
    entryXList[i-1].insert(0, str(X))
    entryYList[i-1].insert(0, str(Y))

def findPosition():
    if tasksStarted:
        return
    if i == 0:
        root.after(50, startFindPos)
        return
    if keyboard.is_pressed('f11'):
        getPosition()
    root.after(50, startFindPos)



def startFindPos():
    threading.Thread(target=findPosition).start()


addTask()
startFindPos()
root.mainloop()





