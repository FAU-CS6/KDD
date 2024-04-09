# Imports
import os
import tempfile
import shutil
import re
import subprocess
from argparse import ArgumentParser


# Helper functions to check command line input
def valid_dir(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def valid_tex_file(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string + " does not exist")


def remove_tex_ending(string):
    if string.endswith(".tex"):
        return string[:-4]
    else:
        return string


# Helper function to compile the LaTeX files
def compile_latex_files(input, output_folder, style):
    # Check if input is a valid file without the .tex ending
    valid_tex_file(input + ".tex")

    # Create a temp folder to store the build artifacts
    temp_folder = tempfile.mkdtemp()

    # Call the latexmk command to compile the .tex file
    command = [
        "latexmk",
        "-pdf",
        "-pdflatex=pdflatex -interaction=nonstopmode -shell-escape -synctex=1 %O '\input{%S}'",
        "--interaction=nonstopmode",
        "-shell-escape",
        "-silent",
        "-f",
        f"-output-directory={temp_folder}",
        f"{input}.tex",
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        print("Created LaTeX files successfully.")
        print("Output:", result.stdout.decode())
    else:
        print("Error while creating the LaTeX files.")
        print("Error:", result.stderr.decode())

    # Copy the pdf from the temp folder to the output folder
    shutil.copy(os.path.join(temp_folder, input + ".pdf"), output_folder)


if __name__ == "__main__":
    # Handle the command line input
    parser = ArgumentParser()
    parser.add_argument("input", type=valid_tex_file)
    parser.add_argument("-o", "--output", dest="output", required=True)
    args = parser.parse_args()

    # Check if the output directory exists
    if not os.path.isdir(args.output):
        os.makedirs(args.output)

    # Remove the .tex ending from the input file
    input_without_ending = remove_tex_ending(args.input)

    # Build the LaTeX-files
    compile_latex_files(input_without_ending, args.output, args.style)
