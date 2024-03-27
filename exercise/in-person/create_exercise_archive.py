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


def valid_style(string):
    if string == "original" or string == "student" or string == "solution":
        return string
    else:
        raise Exception(str(string) + " is not a valid style")


# Helper function to create the zip file for the additional files
def create_additional_files_zip(input_folder, output_folder, style):
    # Copy the input directory into a temp folder
    temp_folder = tempfile.mkdtemp()
    folder_name = os.path.basename(os.path.normpath(args.input))
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
    shutil.make_archive(output_folder, "zip", folder_temp_path)


# Helper function to compile the LaTeX files
def compile_latex_files(input_folder, output_folder):
    # For every .tex file in the input folder
    for file in os.listdir(input_folder):
        if re.match(r"^[A-Za-z0-9._-]*.tex$", file):
            # Call the latexmk command to compile the .tex file
            command = [
                "latexmk",
                "-pdf",
                "--interaction=nonstopmode",
                "-shell-escape",
                "-silent",
                "-f",
                f"-output-directory={output_folder}",
                file,
            ]

            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            if result.returncode == 0:
                print("Created LaTeX files successfully.")
                print("Output:", result.stdout.decode())
            else:
                print("Error while creating the LaTeX files.")
                print("Error:", result.stderr.decode())


if __name__ == "__main__":
    # Handle the command line input
    parser = ArgumentParser()
    parser.add_argument("input", type=valid_dir)
    parser.add_argument("-o", "--output", dest="output", required=True)
    parser.add_argument(
        "-s", "--style", dest="style", default="original", type=valid_style
    )
    args = parser.parse_args()

    # Build the LaTeX-files
    compile_latex_files(args.input, args.output)

    # If there is an folder starting with "Additional-Files" in the input directory, call the create_additional_files_zip helper to create a corresponding zip folder
    for file in os.listdir(args.input):
        if re.match(r"^Additional-Files.*", file):
            create_additional_files_zip(
                os.path.join(args.input, file),
                os.path.join(args.output, file),
                args.style,
            )
            break
