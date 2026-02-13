import os

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if valid_target_dir == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    file_valid = os.path.isfile(os.path.join(working_dir_abs, file_path))
    if file_valid == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file, 'r') as x:
            content = x.read(10000)
            if x.read(1):
                content += f'[...File "{file_path}" truncated at 10000 characters]'
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."

    return content