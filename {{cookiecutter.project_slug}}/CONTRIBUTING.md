Contributing Guide
==================

Bug Reports
-----------

For bug reports or requests{% if 'github.com' in cookiecutter.repository or 'gitlab.com' in cookiecutter.repository %} submit an issue: <{{ cookiecutter.repository }}/issues>{% else %} send me an email to <{{ cookiecutter.email }}>.{% endif %}

Pull Requests
-------------

Contributions are welcome and greatly appreciated!

To develop new features or bug fixes follow this workflow:

1. Fork the {{ cookiecutter.project_name }} repository: <{{ cookiecutter.repository }}>

2. Obtain the source by cloning it onto your development machine::

    git clone {{ cookiecutter.repository }}
    cd {{ cookiecutter.project_slug }}

3. Create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature

4. Create and activate a Python virtual environment for local development::

    doit install

5. Now you can develop your fix or enhancement. Update existing unit tests or create a new ones to verify the change works as expected. Run the test suite, style compliance checks and code coverage with::

    doit

6. You can get more info of the developer tasks with::

    doit list

7. If all test are passed, commit and push changes to your fork. ::

    git add .
    git commit -m "A detailed description of the changes."
    git push origin name-of-your-bugfix-or-feature

8. Finally, go to the web page of your fork and make a pull request to the {{ cookiecutter.project_name }} repository.
{% if 'github.com' in cookiecutter.repository %}<https://help.github.com/articles/about-pull-requests/>{% elif 'gitlab.com' in cookiecutter.repository %}<https://docs.gitlab.com/ee/gitlab-basics/add-merge-request.html>{% endif %}
