# -*- coding: utf-8 -*-
import subprocess


def git_clone(project, url, workspace):
    cmd = ['git', 'clone', url]
    print "Cloning %s into %s" % (project, workspace)
    p = subprocess.Popen(cmd, cwd=workspace)
    p.wait()
