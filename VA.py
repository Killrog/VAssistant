import os
import json
import subprocess

#python -m PyInstaller --onefile my_assistant.py ... to create new exe 
#Line to read json for useable commands
#. voiceenv\Scripts\activate to activate the venv in case its not showing in BASH terminal
#no clue why this time I need a . before it but that works so idcpip i
COMMANDS = {}

try:
    with open("Commands.json", "r",encoding="utf-8") as f:
        COMMANDS = json.load(f)
except FileNotFoundError:
    print("commands.json not found only built in commands will work.")
except json.JSONDecodeError:
    print("commands.json has bad format (invalid JSON)")
    



# def add_task():
    


# def manage_tasks():

# def remove_task():


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


    while True:
        command = input().strip()                                       # .strip() removes extra spaces
       
        if command.lower() in ["exit", "stop"]:
            print("AI Assistant Deactivated.")
            break
        
        elif command.lower() == "bootup protocol":  #test for bootup protocol:
            bootup_protocol()
            continue

        if not command:
            continue  # Skip empty input

        response = respond_to_command(command)
        print("AI: ", response)


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

if __name__ == "__main__":
    run_assistant()

