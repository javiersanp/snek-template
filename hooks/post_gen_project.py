import os
import shutil
import subprocess

if __name__ == "__main__":
    project_directory = os.path.realpath(os.path.curdir)
    os.chdir(project_directory)
    if "{{ cookiecutter.license }}" == "Not open source":
        os.remove("LICENSE")
    subprocess.run(["python", os.path.join("bin", "verchew")])
    if "{{ cookiecutter.docs_generator }}" == "Sphinx":
        shutil.rmtree("docs")
        os.rename("sphinx", "docs")
        os.remove("mkdocs.yml")
    else:
        shutil.rmtree("sphinx")
        os.remove(os.path.join("bin", "serve-docs"))
    cli = "{{ cookiecutter.command_line_interface }}"
    if cli == "No command-line interface":
        os.remove(os.path.join("{{ cookiecutter.project_slug }}", "cli.py"))
        os.remove(
            os.path.join("{{ cookiecutter.project_slug }}", "__main__.py")
        )
        os.remove(os.path.join("tests", "test_cli.py"))
    if "{{ cookiecutter.continous_integration }}" != "Travis":
        os.remove(os.path.join(".travis.yml"))
    if "{{ cookiecutter.continous_integration }}" != "CircleCI":
        shutil.rmtree(".circleci")
