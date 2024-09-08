import subprocess
import os
script1 =os.getcwd()+'\\Broker\\main.py'
script2=os.getcwd()+'\\UE\\main.py'
script3 =os.getcwd()+'\\Resource\\main.py'

# Function to run a script in a new command prompt window
def run_script(script_path):
    subprocess.Popen(['start', 'cmd', '/k', 'python', script_path], shell=True)

# # Run the scripts
run_script(script1)
run_script(script2)
run_script(script3)

    