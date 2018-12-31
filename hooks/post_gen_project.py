import os
import subprocess

if __name__ == "__main__":
    project_directory = os.path.realpath(os.path.curdir)
    os.chdir(project_directory)
    os.remove("extra_context.j2")
    if "{{ cookiecutter.license }}" == "Not open source":
        os.remove("LICENSE")
    subprocess.run(["python", os.path.join("bin", "verchew")])
