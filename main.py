import subprocess
import os
import signal
import time
from Config import Config
script1 =os.getcwd()+'\\Broker\\main.py'
script2=os.getcwd()+'\\UE\\main.py'
script3 =os.getcwd()+'\\Resource\\main.py'

# Function to run a script in a new command prompt window
def run_script(script_path):
    process=subprocess.Popen(['start', 'cmd', '/k', 'python', script_path], shell=True)
    process.wait()
  
def start_programs_2_and_3():
    program2 = subprocess.Popen(['python', os.getcwd()+'\\Broker\\main.py'], shell=True)
    program3 = subprocess.Popen(['python', os.getcwd()+'\\Resource\\main.py'], shell=True)
    return program2, program3

# Function to kill programs 2 and 3
def kill_programs(program2, program3):
    if program2.poll() is None:  # Check if program 2 is still running
        os.kill(program2.pid, signal.SIGTERM)  # Kill program 2
    if program3.poll() is None:  # Check if program 3 is still running
        os.kill(program3.pid, signal.SIGTERM)  # Kill program 3

config=Config()
rep_np=config.get_config("Global","repeat")
for i in range(rep_np):
    # Step 1: Start programs 2 and 3
    program2, program3 = start_programs_2_and_3()
    print("Started programs 2 and 3")

    # Step 2: Run program 1 and wait for it to finish
    print("Running program 1...")
    program1 = subprocess.Popen(['python',os.getcwd()+'\\UE\\main.py'], shell=True)
    program1.wait()  # Wait for program 1 to complete
    print("Program 1 finished")

    # Step 3: Kill programs 2 and 3
    print("Killing programs 2 and 3...")
    kill_programs(program2, program3)
    

