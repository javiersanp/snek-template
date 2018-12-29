"""Script for task automation.

See: http://pydoit.org/
"""
import glob

DOIT_CONFIG = {
    # 'default_tasks': []
    'verbosity': 2
}

PYTHON_FILES = glob.glob('**/*.py', recursive=True)


def temp_task_install():
    """Install all dependencies in .venv virtual environment."""
    return {
        'file_dep': ['pyproject.toml'],
        'actions': ['poetry install'],
    }


def task_style():
    """Check code styling."""
    for action in ['flake8', 'pydocstyle', 'isort --check-only -rc .']:
        yield {
            'file_dep': PYTHON_FILES,
            'name': action.split(' ')[0],
            'actions': [action],
        }
