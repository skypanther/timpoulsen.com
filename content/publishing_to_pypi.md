Title: Publishing to PyPI
Date: January 25, 2019
Category: Python
Tags: python

I recently published my first [Python package](https://pypi.org/project/robovision/) to [PyPI](https://pypi.org/). The guides I found on how to do so were mostly out-of-date and confusing. Of course, PyPI is reportedly coming out with new updates soon and my instructions here will soon be outdated. In any case, here's my take on how you can publish your own project.

(_Note, the following guide will work for OS X and Linux. You'll need to make some adjustments for Windows, which I apologize but I'm unable to provide guidance for._)

I recommend you start right and use [CookieCutter](https://github.com/audreyr/cookiecutter) to create the shell of your project. There are a couple of Python [package templates](https://github.com/audreyr/cookiecutter#python) that will give you the shell of what you need. (I used the cookiecutter-pypackage-minimal template, but the "ultimate" template might fit your needs better.)

Many guides suggest you reserve your package's name on PyPI right away so that no one else "steals" it. However, PyPI no longer supports package name reservations. The best you can do is search ahead of time to be reasonably sure your chosen name is not already taken.

## Local package installation

As you develop, you can test that your package is installable and working by installing it from your local folder. Use `pip` to install from your development folder:

```
cd path/to/your/package/folder
pip install -e .
```

## PyPI registration

Once your package is ready, you'll need to create accounts on both [pypi.org](https://pypi.org/account/register/) and [test.pypi.org](https://test.pypi.org/account/register/). PyPI says those systems will be linked eventually. But for now, the test and production environments are completely separate. You can use the same information to register for both sites.

## The `twine` package uploader

You'll be using `twine` to upload your package to PyPI. Let's get that set up. First, install it with:

```
pip install twine
```

You'll need to create a configuration file in your home directory. Using your favorite code editor, create a file named `.pypirc` in your home directory with the following contents:

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

Take note that there's no `repository` line for the pypi (production) entry. Previous versions of twine required that line but it will cause an error with current versions.

## Configure distribution options

You'll need to choose between the [wheel and egg](https://packaging.python.org/discussions/wheel-vs-egg/) packaging formats. In most cases, you'll want to choose wheel. See the linked guide if you think you might need to use the older egg format.

Next, you're going to need to make sure you have a few files in your package directory. If you used one of the CookieCutter templates I linked to above, you'll have these. But, you'll need to make sure they're updated with correct information.

Use the ReStructuredText format for your readme or the info on the PyPI site will be all borked up. That means you'll need a `README.rst` file in the root directory of your project. Supposedly PyPI supports Markdown but don't believe them. Most code repositories (GitHub, etc.) support ReStructuredText readmes, so you don't need to create multiple files.

Make sure to include a LICENSE and/or LICENSE.md file to announce your package's license.

You'll need to update the setup.cfg file to reflect your package publishing options. First, assuming you're using the wheel format, you'll need to set `universal=1` for a package that targets _both_ Python 2.x and Python 3.x or `universal=0` if targeting just Python 3.x. Second, make sure the `description-file` references your readme file's name. Here's my setup.cfg:

```
[bdist_wheel]
universal=0

[metadata]
description-file=README.rst
```

Assuming you used CookieCutter, you should have already configured the basics of the setup.py file. It notes various settings and is used by `setuptools` to create your distribution file. Make sure that the version number, readme file name, license, and other options are correct for your package.

Note that if you have Python files in subdirectories off your main package folder, you'll need to list them in the `packages=[]` list. See [my setup.py file](https://github.com/skypanther/robovision/blob/master/setup.py) and my source code organization if this doesn't make sense to you.

## Create your distribution file

With all that configuration out of the way, you're ready to create your distribution wheel file. Use this command:

```
python setup.py bdist_wheel
```

This will package up your file and create a wheel file in the dist directory in your project. 

## Uploading

You should upload to the test environment first, and install your package from the test environment. That way, you're assured everything is working as expected before you announce your package to the world. Use this command:

```
twine upload dist/YOUR_PACKAGE_NAME.whl -r testpypi
```

Use a command like this to install from the test environment:

```
pip install -i https://test.pypi.org/simple YOUR_PACKAGE_NAME
```

Once you're sure everything is in order, upload to the production PyPI server:

```
twine upload dist/YOUR_PACKAGE_NAME.whl
```

Congratulations! You've published a Python package to PyPI.

## Updating your package

Going forward, as you make improvements and additions to your library, you'll need to do just a couple of things to publish an update.

* First, update setup.py with the new version number
* Update your readme to note any new features, and probably new version number
* Use `python setup.py bdist_wheel` to create a new distribution file
* Use `twine upload dist/YOUR_PACKAGE_NAME.whl` to upload it

