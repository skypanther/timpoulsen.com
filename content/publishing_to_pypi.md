Title: Publishing to PyPI
Date: January 18, 2019
Category: Python
Tags: python
Status: draft


Register accounts on pypi.org and test.pypi.org

Use cookiecutter (link) and one of the python package templates.

`pip install twine`

Set up your .pypirc file:

```
[distutils]
index-servers=
    testpypi
    pypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = your_username
password = your_password

[pypi]
username = your_username
password = your_password
```

Note: No `repository` line for the pypi entry

Choose your packaging format (link)

Then `python setup.py bdist_wheel` to create your distribution tar.gz file

Then, upload first to test:

`twine upload dist/YOUR_PACKAGE_NAME.whl -r testpypi`

Confirm it's there, do a test install, make sure it all works.

Then, upload to the live server:

`twine upload dist/YOUR_PACKAGE_NAME.whl`



first paragraph

Syntax highlighting with & without line numbers

    :::python
    print("The triple-colon syntax will *not* show line numbers.")

To display line numbers, use a path-less shebang instead of colons:

    #!python
    print("The path-less shebang syntax *will* show line numbers.")

    #!javascript
    sample code block

Include font-awesome symbols like this
<i class="fa fa-heart red"></i>