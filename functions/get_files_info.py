import os


def get_files_info(working_directory: str, directory: str=".") -> str:
    items_in_directory = ""
    try:
        absolute_path = os.path.abspath(working_directory)
    
        target_directory = os.path.normpath(os.path.join(absolute_path, directory))
        is_valid_path = os.path.commonpath([absolute_path, target_directory]) == absolute_path
        if not is_valid_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'
        for item in os.listdir(target_directory):
            try:
                item_name = item
                item_file_size = os.path.getsize(os.path.join(target_directory, item))
                item_is_directory = os.path.isdir(os.path.join(target_directory, item))
                item_string = f'{item_name}: file_size={item_file_size}, is_dir={item_is_directory}'
                items_in_directory += "-" + item_string + "\n"
            except Exception as e:
                return f'Error: {e}'
        return items_in_directory
    except Exception as e:
        return f'Error: {e}'


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
    