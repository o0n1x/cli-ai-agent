import os


def get_files_info(working_directory, directory="."):
    try:
        path = os.path.join(working_directory, directory)

        if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{path}" as it is outside the permitted working directory'
        if not os.path.isdir(path):
            return f'Error: "{path}" is not a directory'
    except Exception as e:
        return f"Error: {e}"
    
    
    rslt = ""
    if directory == ".":
        rslt += "Result for current directory:"
    else:
        rslt += f"Result for {directory} directory:"
        
    try:
        for file in os.scandir(path):
            rslt += f"\n- {file.name}: file_size={os.path.getsize(file.path)} bytes, is_dir={file.is_dir()}"
        return rslt
    except Exception as e:
        return f"Error: {e}"
