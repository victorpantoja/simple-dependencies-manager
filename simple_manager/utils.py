# -*- coding: utf-8 -*-
import os
import subprocess


def git_clone(project, url, workspace):
    cmd = ['git', 'clone', url]
    print "Cloning %s into %s" % (project, workspace)
    p = subprocess.Popen(cmd, cwd=workspace)
    p.wait()


def git_add(project, workspace):
    path = os.path.join(workspace, project)
    cmd = ['git', 'add', "."]
    print("Adding new files to {0}").format(path)
    p = subprocess.Popen(cmd, cwd=path)
    p.wait()


def git_commit(workspace, project):
    path = os.path.join(workspace, project)
    print("Committing changes to {0}").format(path)
    cmd = "git commit -am 'Moving project do new package'"
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=path).stdout.read()


def git_push(project, workspace):
    path = os.path.join(workspace, project)
    print("Sending changes of {0} to remote server").format(project)
    cmd = ['git', 'push']
    p = subprocess.Popen(cmd, cwd=path)
    p.wait()
