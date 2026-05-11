import os
import json
import subprocess

#python -m PyInstaller --onefile VA.py ... to create new exe 
#Line to read json for useable commands
#. voiceenv\Scripts\activate to activate the venv in case its not showing in BASH terminal
#no clue why this time I need a . before it but that works so idc pip i
COMMANDS = {}

try:
    with open("Commands.json", "r",encoding="utf-8") as f:
        COMMANDS = json.load(f)
except FileNotFoundError:
    print("commands.json not found only built in commands will work.")
except json.JSONDecodeError:
    print("commands.json has bad format (invalid JSON)")
    

tasklist_file ="tasklist.json"

def load_tasklist():
    if not os.path.exists(tasklist_file):
        print("No tasklist found, starting with an empty tasklist.")
        return []
    try:
        with open(tasklist_file, "r",encoding="utf-8") as f:
            print("successfully loaded tasklist.")
            return json.load(f)
    except (json.JSONDecodeError, IOError):
           return []  # Return empty list if file is corrupted or can't be read


def add_task(tasklist):

    print("Adding a new task.")

    print("Enter task title...")
    title = input(" Title: ").strip()

    print("Enter task date (DD.MM.YYYY)...")
    date = input(" Date: ").strip()

    print("Enter task time (HH:MM)...")
    time = input(" Time: ").strip()

    print("Enter task description...")
    description = input(" Description: ").strip()

    print("Enter any custom information (optional)...")
    custom = input(" Custom: ").strip()

    

    task = {
        "title": title,
        "date": date,
        "time": time,
        "description": description,
        "custom": custom
    }

    tasklist.append(task)
    save_tasklist(tasklist)
    print("task added successfully.")



def view_tasklist():
    if tasklist:
        for task in tasklist: 
            print("") #one empty space for better visibilty in console       
            print("Task Details:")
            for data, value in task.items():
                print(f"{data}: {value}")
            
            print("__________________________")#for spacing in between tasks
            
                
    else:
        print("No tasks in the list.")    
    #print(tasklist) #print entire list


def edit_task():
    print("To edit a task select one via order of the list (Starts at 0)")
    task_number_str = input("Number: ").strip()

    if not task_number_str.isdigit():
        print("Invalid task number.")
        return

    task_number = int(task_number_str)
    if task_number < 0 or task_number >= len(tasklist):
        print("Task number out of range.")
        return

    task = tasklist[task_number]
    print("Choose the parameter you want to change (title, date, time, description, custom)")
    variable = input("Task parameter: ").strip()

    if variable not in task:
        print(f"Unknown task parameter: {variable}")
        return

    task[variable] = input(f"change {variable} to: ").strip()
    save_tasklist(tasklist)
    print(f"Updated task {task_number}: {variable} = {task[variable]}")


def remove_task():
    #decided to not use the deletion by number here FOR NOW will take the best solution when I have feedback
    
    task_title = input("Enter task title to delete task: ").strip()
    

    for task in tasklist:
        if task.get("title") == task_title:
            tasklist.remove(task)
            save_tasklist(tasklist)
            print(f"succesfully removed task {task}")
            return
            
            

def save_tasklist(tasks): 
    try: 
        with open(tasklist_file,"w", encoding="utf-8") as f:
           json.dump(tasks,f , indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving tasklist: {e}")





#   -   -   -  test for "bootup protocol    -   -   -"
def bootup_protocol():
    print("AI: Booting up Initial Applications")
    respond_to_command("steam")
    respond_to_command("discord")
    respond_to_command("bnet")
    print("opening steam,opening battle.net,opening discord)")
    #works will finish this in the future with whatever I will need then
    #maybe change for command for bootup or if poss make it a button in the app
    

#   -   -   -   function to respond to the terminal input   -   -   -
def respond_to_command(command):

    cmd = command.lower().strip()  # Normalize the command for matching (Still here from AI but I keep it for awareness that this SHOULD be useless to strip and lower again)
    

    if cmd in COMMANDS:
        entry = COMMANDS[cmd]
        typ = entry.get("type", "unknown")  # Default to "unknown" if type is not specified


        if typ == "exe":
            path = entry.get("path")
            if path and os.path.isfile(path):
                os.startfile(path)
                return entry.get("response", f"Executing {cmd}.")
                #except Exception as e:      #e is for print statement for debugging 
                 
            else:
                return f"Path for {cmd} is invalid or does not exist"



        elif typ == "text":
            return entry.get("response", f"Executing {cmd}.") #after , is basicly failsafe when no value is in response

        elif typ == "close":
            print("disabled for risk of mistakes and probably unnessary eitherway")
            # proc = entry.get("process")
            # if not proc:
            #     return "No process specified for closet command."
            
            # msg = entry.get("response", f"closing {cmd}.")

            # try:
            #     subprocess.run(["taskkill", "/F", "/IM", proc], check=True,capture_output=True)                   
            #     return msg
            # except subprocess.CalledProcessError as e:
            #     if "not found" in e.stderr.decode().lower():
            #         return f"Process {proc} not running (or already closed)."
            #     else:
            #         return f"Failed to close {cmd}:{e}"
            # except Exception as e:
            #     return f"Error while trying to close {cmd}: {e}"
   
    else:
         return f"Sorry, There is no command for {command}."   
         

#   -   -   -   function to start base assistant (run assistant is being called at the bottom)  -   -   -
def run_assistant():
    print("AI Assistant Activated (Type Exit to deactivate).")
    print("type 'help' for info about commands")


    while True:
        command = input().strip()                                       # .strip() removes extra spaces
       
        if command.lower() in ["exit", "stop"]:
            print("AI Assistant Deactivated.")
            break
        
        elif command.lower() == "bootup protocol":  #test for bootup protocol:
            bootup_protocol()
            continue

        elif command.lower() in ["add task","add"]:             
            add_task(tasklist)
            continue

        elif command.lower() in ["view tasklist","view"]:             
            view_tasklist()
            continue

        elif command.lower() in ["remove task","delete task", "remove", "delete","del"]:             
            remove_task()
            continue

        elif command.lower() in ["edit task","change task", "edit", "change"]:             
            edit_task()
            continue

        elif command.lower() in ["help"]:             
            help()
            continue


        if not command:
            continue  # Skip empty input

        response = respond_to_command(command)
        print("AI: ", response)


def help():
    print("Currently available Commands are:")
    print("bootup protocol: Launches User set programs (only via code atm)")
    print("add task: Adds a task with different parameters")
    print("view tasklist: Shows you the current list of tasks you set")
    print("remove task: removes specific task")
    print("edit task: changes the chosen parameter of specific task")
    print("(shortcut for these commands can be viewed in the code only atm)")
    print("for feedback or features that would be nice just message me directly (Alexanderhennigbusiness@outlook.de, you don't have to use my mail just use ANYTHING YOU HAVE XD)")

#add function to detect games (probably through ai) and ask for permission
#command = dota -> Would you like to start Dota 2?    or programs like discord etc.
#instead of hardcoding it
#close games either through steams abort/"Anhalten" after launching the game OR just task manager quit
#if it needs to be hard coded do I have to go with the exe everytime or do I have other options?

#stuff that would be nice to add maybe
#-confirmation for dangrous actions
#-open browser pages (preset websites or custom url inputs (advanced maybe safe urls for later quick open))
#-Actual application maybe with graphics instead of terminal
#if app exists somehow let users set apps themselves for bootup AND singular app starts
#better visual when printing tasklist
#add sorting to show the first task as the one closest to the current date (maybe mark ones that happened in a different color or add a special note to those)

if __name__ == "__main__":
    tasklist = load_tasklist()
    run_assistant()
    

