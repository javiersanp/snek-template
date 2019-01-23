{{ cookiecutter.project_name }}
{{cookiecutter.project_name|length * '=' }}

{% if cookiecutter.continous_integration == 'Travis' %}[![](https://travis-ci.org/javiersanp/snek-template.png)](https://travis-ci.org/javiersanp/snek-template) {% elif cookiecutter.continous_integration == 'CircleCI' %}[![](https://circleci.com/gh/javiersanp/snek-template.png?style=shield)](https://travis-ci.org/javiersanp/snek-template){% endif %}

***

{{ cookiecutter.project_short_description }}

Getting started
---------------

TODO: Detailed description of the project

