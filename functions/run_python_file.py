import os
import subprocess
from subprocess import CompletedProcess
def run_python_file(working_directory, file_path, args=[]):
    try:
        path = os.path.join(working_directory, file_path)

        if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(path):
            return f'Error: File "{file_path}" not found.'
        if not path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
    except Exception as e:
        return f"Error: {e} , first block"

    try:
        
        result = subprocess.run(["uv", "run" , path ] + args,timeout=30,capture_output=True,text=True)
        code = result.returncode
        rsltcode = "" if code == 0 else f"Error: executing Python file: {code}"
        rslt = f"\n STDOUT: {result.stdout} \n STDERR: {result.stderr} \n {rsltcode}"
        return rslt
    except Exception as e:
        return f"Error: {e} , second block"
    

