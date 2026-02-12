import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    dir_list = os.listdir(target_dir)
    string_list = []

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if valid_target_dir == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    directory_valid = os.path.isdir(os.path.join(working_dir_abs, directory))
    if directory_valid == False:
        return f'Error: "{directory}" is not a directory'

    for x in dir_list:
        filename = x
        
        try:
            full_path = os.path.join(target_dir, x)
        except Exception as e:
            return f"Error: {e}"
        
        try:
            filesize = os.path.getsize(full_path)
        except Exception as f:
            return f"Error: {f}"
        
        try:
            dir_test = os.path.isdir(full_path)
        except Exception as g:
            return f"Error: {g}"
        
        string_list.append(f"- {filename}: file_size={filesize}, is_dir={dir_test}\n")

    result = "".join(string_list)
    return result