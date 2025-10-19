import os
from config import MAX_FILE_LENGTH_LIMIT


def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory, file_path)

    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(path, "r") as f:
            file_content_string = f.read(MAX_FILE_LENGTH_LIMIT)
            if os.path.getsize(path) > MAX_FILE_LENGTH_LIMIT:
                file_content_string += f'[...File "{path}" truncated at {MAX_FILE_LENGTH_LIMIT} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"


