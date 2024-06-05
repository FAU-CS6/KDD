# Imports
import os
import tempfile
import shutil
import re
import subprocess
from argparse import ArgumentParser
from traitlets.config import Config
from nbconvert.exporters import NotebookExporter
from nbconvert.preprocessors import TagRemovePreprocessor


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


def valid_style(string):
    if string == "original" or string == "student" or string == "solution":
        return string
    else:
        raise Exception(str(string) + " is not a valid style")


# Helper function to create the zip file for the additional files
def create_additional_files_zip(input_folder, output_folder, style):
    # Copy the input directory into a temp folder
    temp_folder = tempfile.mkdtemp()
    folder_name = os.path.basename(os.path.normpath(input_folder))
    folder_temp_path = os.path.join(temp_folder, folder_name)
    shutil.copytree(input_folder, folder_temp_path)

    # If the style is not "original", apply the nbconvert tag removal to every ipynb in the folder
    if style != "original":
        # Setup the Config
        c = Config()

        # Setup the TagRemovePreprocessor
        # For the student style delete the solution tags and for the solution style delete the student tags
        if style == "student":
            c.TagRemovePreprocessor.remove_cell_tags = ("solution",)
        elif style == "solution":
            c.TagRemovePreprocessor.remove_cell_tags = ("student",)

        c.TagRemovePreprocessor.enabled = True

        # Setup the Exporter
        c.NotebookExporter.preprocessors = [
            "nbconvert.preprocessors.TagRemovePreprocessor"
        ]
        exporter = NotebookExporter(config=c)
        exporter.register_preprocessor(TagRemovePreprocessor(config=c), True)

        # Iterate through all files in the copied folder
        for file in os.listdir(folder_temp_path):
            # Check if it is a .ipynb file
            if re.match(r"^[A-Za-z0-9._-]*.ipynb$", file):
                # Delete the cells with the tag
                new_notebook = exporter.from_filename(
                    os.path.join(folder_temp_path, file)
                )

                # Write the new file over the old one
                with open(os.path.join(folder_temp_path, file), "w") as new_file:
                    new_file.write(new_notebook[0])

    # Create a zip out of the copied (and modified) folder
    if style == "student":
        shutil.make_archive(
            output_folder + "/Additional-Files-Student", "zip", folder_temp_path
        )
    elif style == "solution":
        shutil.make_archive(
            output_folder + "/Additional-Files-Solution", "zip", folder_temp_path
        )


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

    # If the style is solution, add the solutionsflag to the command
    if style == "solution":
        command = [
            "latexmk",
            "-pdf",
            "-pdflatex=pdflatex -interaction=nonstopmode -shell-escape -synctex=1 %O '\def\solutionsflag{}\input{%S}'",
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

    # Rename the output pdf to include a -Student or -Solution suffix
    if style == "student":
        os.rename(
            os.path.join(temp_folder, input + ".pdf"),
            os.path.join(temp_folder, input + "-Student.pdf"),
        )

        # Copy the pdf from the temp folder to the output folder
        shutil.copy(os.path.join(temp_folder, input + "-Student.pdf"), output_folder)
    elif style == "solution":
        os.rename(
            os.path.join(temp_folder, input + ".pdf"),
            os.path.join(temp_folder, input + "-Solution.pdf"),
        )

        # Copy the pdf from the temp folder to the output folder
        shutil.copy(os.path.join(temp_folder, input + "-Solution.pdf"), output_folder)


if __name__ == "__main__":
    # Handle the command line input
    parser = ArgumentParser()
    parser.add_argument("input", type=valid_tex_file)
    parser.add_argument("-o", "--output", dest="output", required=True)
    parser.add_argument(
        "-s", "--style", dest="style", default="original", type=valid_style
    )
    args = parser.parse_args()

    # Create a temp folder to later convert into a zip folder
    temp_folder = tempfile.mkdtemp()

    # Remove the .tex ending from the input file
    input_without_ending = remove_tex_ending(args.input)

    # Build the LaTeX-files
    compile_latex_files(input_without_ending, temp_folder, args.style)

    # If there is an folder with input_without_ending name, call the create_additional_files_zip helper to create a corresponding zip folder
    if os.path.exists(input_without_ending):
        create_additional_files_zip(
            input_without_ending,
            temp_folder,
            args.style,
        )

    # Create a zip for all exercise content
    suffix = "-Student"

    if args.style == "solution":
        suffix = "-Solution"

    shutil.make_archive(
        args.output + "/" + input_without_ending + suffix, "zip", temp_folder
    )
