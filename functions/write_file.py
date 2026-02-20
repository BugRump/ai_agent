import os
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes a provided string into a targeted file relative to the working directory, creating necessary file and directory branches if they do not already exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the intended file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="a string that will be written into the targeted file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
    a = os.path.dirname(file_path)
    b = os.path.normpath(os.path.join(working_dir_abs, a))
    d = os.path.normpath(os.path.join(working_directory, file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if valid_target_dir == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    directory_valid = os.path.isdir(os.path.join(working_dir_abs, file_path))
    if directory_valid:
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        os.makedirs(b, exist_ok=True)
    except Exception as e:
        return f"Error: {e}"
    
    try:
        with open(d, "w") as f:
            f.write(content)
    except Exception as g:
        return f"Error: {g}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    
