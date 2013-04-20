simple-dependencies-manager
===========================

Imagine this scenario: you are a software engineer and works in a somewhat big project and have dependencies for another projects of yours.

For example, you're now working at project_a that has depencies of project_b and project_c. Both project_b and project_c are pypi projects and project_a demands any channges in b and c.

Now imagine yourself hard developing project_a that demands lots of changes in project_b and project_c. And you have to package both dependencies each producition deployment you do.

Sounds crazy? Yeah...

With simple-dependencies-manager, you can create a new version of your dependencies, pull versions to git and upload to your egg repository.

As simple as:
$ python simple-manager -f config.yaml --(pull|clone|push)

This way, you will pull both project from git.


CHANGE LOG
----------
### 0.2.0: Managing tags
You can easily tag all your projects in only one command:

python simple-manager.py -f config.yaml -r YOUR_PROJECT_ -t

User will be shown de last project's tag and will be promped to enter a new one and also a description.

### 0.1.0: First version. Things like cloning, pushing and pulling implemented

RELEASE PLAN
------------
### 0.3.0: Install dependencies