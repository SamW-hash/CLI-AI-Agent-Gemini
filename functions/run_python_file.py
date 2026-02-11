import os, subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs valid python files via subprocess at a specified file path relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run files from, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments passed to the file being ran. Arguments will be relative to the nature of the file being ran. Default is None. If present, they should be declared after file_path"
            ),
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_dir.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_dir]
        if args != None:
            command.extend(args)
        result = subprocess.run(
            command, 
            cwd=working_dir_abs, 
            capture_output=True,
            text=True,
            timeout=30)
        output_message = []
        if result.returncode != 0:
            output_message.append(f"Process exited with code {result.returncode}")
        if not result.stderr and not result.stdout:
            output_message.append("No output produced")
        if result.stdout:
            output_message.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output_message.append(f"STDERR: {result.stderr}")

    except Exception as e:
        return f"Error: executing Python file: {e}"
    return "".join(output_message)

        
