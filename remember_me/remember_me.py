####
# File deletion
####

import pathlib  
pathlib.Path.unlink(f"processes\whatever.json") 

###
# Opening anaconda within a Python script
###
import subprocess

# Activate the conda environment and list the environments
command = 'C:\\Users\\User\\AppData\\Local\\anaconda3\\Scripts\\activate.bat && conda env list'
result = subprocess.run(command, shell=True, capture_output=True, text=True)

# Print the output
print(result.stdout)