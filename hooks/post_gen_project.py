import os

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == "__main__":

    remove_file("extra_context.j2")
    if "{{ cookiecutter.license }}" == "Not open source":
        remove_file("LICENSE")
