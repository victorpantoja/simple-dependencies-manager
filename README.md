simple-dependencies-manager
===========================

Imagine this scenario: you are a software engineer and works in a somewhat big project and have dependencies for another projects of yours.

For example, you're now working at project_a that has depencies of project_b and project_c. Both project_b and project_c are pypi projects and project_a demands any channges in b and c.

Now imagine yourself hard developing project_a that demands lots of changes in project_b and project_c. And you have to package both dependencies each producition deployment you do.

Sounds crazy? Yeah...

With simple-dependencies-manager, you can create a new version of your dependencies, pull versions to git and upload to your egg repository.

As simple as:
$ python simple-manager --version project_b==1.1.0 --version project_c==0.2.1

This command will create tags 1.1.0 and 0.2.1, package both projects and upload those new versions to pypi. Also, your requirements file will be updated.

You can update your projects:
$ python simple-manager --update project_b --update project_c

This way, you will pull both project from git.


CHANGE LOG
==========
0.1.0: First version. Things like cloning, pushing and pulling implemented