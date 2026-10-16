import os

def write_file(working_directory, file_path, content):
    try:
        absolute_path = os.path.abspath(working_directory)
        normalized_path = os.path.normpath(os.path.join(absolute_path, file_path))
        if os.path.commonpath([absolute_path, normalized_path]) != absolute_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory.'
        if os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory.'
        os.makedirs(os.path.dirname(normalized_path), exist_ok=True)
        with open(normalized_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'