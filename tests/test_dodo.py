import dodo


def test_get_subtask_defaults():
    task = dodo.get_subtask("foo bar")
    assert task["name"] == "foo"
    assert task["actions"] == ["foo bar"]
    assert "file_dep" not in task


def test_get_subtask_with_file_dep():
    task = dodo.get_subtask("foo bar", "taz")
    assert task["name"] == "foo"
    assert task["actions"] == ["foo bar"]
    assert task["file_dep"] == "taz"


def test_get_subtask_with_poetry():
    task = dodo.get_subtask("poetry run foo bar")
    assert task["name"] == "foo"
    assert task["actions"] == ["poetry run foo bar"]
