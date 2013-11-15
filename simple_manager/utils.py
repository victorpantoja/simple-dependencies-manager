# -*- coding: utf-8 -*-
import os
import subprocess


def git_add(project, workspace):
    path = os.path.join(workspace, project)
    cmd = ['git', 'add', "."]
    print("Adding new files to {0}").format(path)
    p = subprocess.Popen(cmd, cwd=path)
    p.wait()


def git_clone(project, url, workspace):
    cmd = ['git', 'clone', url]
    print "Cloning %s into %s" % (project, workspace)
    p = subprocess.Popen(cmd, cwd=workspace)
    p.wait()


def git_commit(workspace, project):
    path = os.path.join(workspace, project)
    print("Committing changes to {0}").format(path)
    cmd = "git commit -am 'Moving project do new package'"
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=path).stdout.read()


def git_push_branch(workspace, project, branch):
    path = os.path.join(workspace, project)
    print("Pushing branch ").format(branch)
    cmd = "git push origin {0}".format(branch)
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=path).stdout.read()


def git_push(project, workspace):
    path = os.path.join(workspace, project)
    print("Sending changes of {0} to remote server").format(project)
    cmd = ['git', 'push']
    p = subprocess.Popen(cmd, cwd=path)
    p.wait()


def git_push_tag(workspace, project):
    cmd = 'git push --tags'
    cwd = '%s/%s' % (workspace, project)
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=cwd).stdout.read()


def git_tag(workspace, project, version, description):
    git_update(workspace, project)

    cmd = 'git tag -a %s -m "%s"' % (version, description)
    cwd = '%s/%s' % (workspace, project)

    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=cwd).stdout.read()


def git_update(workspace, project):
    print "Updating %s" % project
    cmd = ['git', 'pull']
    p = subprocess.Popen(cmd, cwd=workspace + '/' + project)
    p.wait()


def git_status(workspace, project):
    print "Verifying status for %s" % project
    cmd = ['git', 'status']
    p = subprocess.Popen(cmd, cwd=workspace + '/' + project)
    p.wait()


def get_last_tag(workspace, project):
    cmd = 'git describe --tags `git rev-list --tags --max-count=1`'
    cwd = '%s/%s' % (workspace, project)

    try:
        tag = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=cwd).stdout.read()
        print "Last tag for %s: %s" % (project, tag.replace("\n", ""))
        return tag
    except:
        print "No tags found for %s" % project
