Title: How to find outdated Python requirements
Description: Tips for finding outdated Python packages on your system including top-level and dependencies.
Date: April 7, 2024
Category: Python
Tags: python
Slug: finding-outdated-python-packages

# Finding outdated Python packages

A quick Python technique this time. You can get a list of outdated Python packages installed on your system with a simple command:

    :::bash
    pip list --outdated

That will list all the packages, including their dependencies. That's nice, but sometimes it makes it hard to know what to update first. So instead, use this command:

    :::bash
    pip list --outdated --not-required

This will list only top-level packages, not their dependencies.

Do you use developer-only ("dev dependencies") packages, such as unit testing packages? There does not seem to be a simple command to find outdated dev-only packages. The best I can come up with is to install the dev dependencies, then use `pip list`, like this:

    :::bash
    python3 -m venv temp_venv  # create a temp virtual environment
    source temp_venv/bin/activate
    pip install -r requirements-dev.txt  # install the dev dependencies
    pip list --outdated --not-required
    # then deactivate and delete the temp_venv folder

Without the `--outdated` flag, the `pip list` command will list the packages installed in your current environment. You can use the `--not-required` flag to again list only top-level packages.

You can use the `--format json` flag to output the list of packages as JSON. This could be useful if you're going to parse the list programatically. As long as you're not using the `--outdated` flag, you can use `--format freeze` option to output the list of packages in the `pip freeze` style.

You can learn about these and other pip list flags at <a href="https://pip.pypa.io/en/stable/cli/pip_list/" target="_blank">the Pip documentation site</a>.
