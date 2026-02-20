import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes python files in a specified directory relative to the working directory, providing function results as well as their associated stdout and stderr when successful. Otherwise provides error messages specific to various path or other miscellaneous errors.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="a file path relative to the working directory of the python file to be executed. (Must be a .py file and must be within the working directory or its subdirectories)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An array of arguments to be passed into a function call within a python file. (Defaults to None when no argument is passed)",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Argument to be passed into a function call within a python file. (Must be passed in as an array, even if only passing in one argument)"
                ),
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    
    file_directory = os.path.dirname(file_path)
    absolute_file_directory = os.path.normpath(os.path.join(working_dir_abs, file_directory))
    absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    file_type_check = file_path[-3:len(file_path)]

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if valid_target_dir == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    file_valid = os.path.isfile(os.path.join(working_dir_abs, file_path))
    if not file_valid:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if file_type_check != ".py":
        return f'Error: "{file_path}" is not a Python file'
    
    try:
        os.makedirs(absolute_file_directory, exist_ok=True)
    except Exception as e:
        return f"Error: {e}"
    
    result_string_list = [f"Result:\n"]
   
    try:
        command = ["python", absolute_file_path]

        if args != None:
         command.extend(args)

        command_result = subprocess.run(command, stdout=None, stderr=None, capture_output=True, text=True, timeout=30)

        if command_result.returncode != 0:
            result_string_list.append(f"Process exited with code {command_result.returncode}. ")
    
        if command_result.stdout == None and command_result.stderr == None:
            result_string_list.append("No output produced.")
        else:
            result_string_list.append(f"STDOUT: {command_result.stdout}.\n")
            result_string_list.append(f"STDERR: {command_result.stderr}.\n")
    except Exception as e:
        return f"Error: executing Python file: {e}"

    result = "".join(result_string_list)

    return result