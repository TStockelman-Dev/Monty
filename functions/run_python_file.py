import os
import subprocess

def run_python_file(working_directory, file_path, args: list[str] | None = None):
    try:
        output_string = ""
        absolute_path = os.path.abspath(working_directory)
        normalized_path = os.path.normpath(os.path.join(absolute_path, file_path))
        if os.path.commonpath([absolute_path, normalized_path]) != absolute_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(normalized_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not normalized_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", normalized_path]
        if args:
            command.extend(args)
        running_process = subprocess.run(command, capture_output=True, timeout=30, text=True)
        if running_process.returncode != 0:
            output_string += f'Process exited with code {running_process.returncode}.'
        if running_process.stdout == None and running_process.stderr == None:
            output_string += "No output produced"
        output_string += "STDOUT: "
        output_string += running_process.stdout
        output_string += "STDERR: "
        output_string += running_process.stderr
        return output_string
    except Exception as e:
        return f'Error: {str(e)}'
