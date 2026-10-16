import os

def get_file_content(working_directory, file_path):
    try:
        absolute_path = os.path.abspath(working_directory)
        normalized_path = os.path.normpath(os.path.join(absolute_path, file_path))
        if os.path.commonpath([absolute_path, normalized_path]) != absolute_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(normalized_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(normalized_path, 'r') as f:
            MAX_CHARACTERS = 10000
            content = f.read(MAX_CHARACTERS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
        return content
    except Exception as e:
        return f'Error: {e}'