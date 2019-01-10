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
