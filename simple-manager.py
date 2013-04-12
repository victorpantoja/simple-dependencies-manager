#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import subprocess
import yaml
import os

config = yaml.load(open("config.yaml", 'r'))
WORKSPACE = config['workspace']

def get_last_tag(repo):
    cmd = 'git describe --tags `git rev-list --tags --max-count=1`'
    
    import pdb; pdb.set_trace()
    p = subprocess.Popen(cmd, cwd=WORKSPACE+'/'+repo)
    p.wait()

def git_clone(repo):
    cmd = ['git', 'clone', repo]
    print "Cloning %s into %s" % (repo_dir, WORKSPACE)
    p = subprocess.Popen(cmd, cwd=WORKSPACE)
    p.wait()

def git_update(repo):
    cmd = ['git', 'pull']
    p = subprocess.Popen(cmd, cwd=WORKSPACE+'/'+repo)
    p.wait()
    
def git_push(repo):
    cmd = ['git', 'push']
    p = subprocess.Popen(cmd, cwd=WORKSPACE+'/'+repo)
    p.wait()

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hu:c:pt",["update=","create=","push=","tags="])
    except getopt.GetoptError:
        print 'Usage: python simple-manager'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'python simple-manager [-chpu] repo'
            sys.exit()
        elif opt in ("-u", "--update"):
            git_update(arg)
        elif opt in ("-c", "--create"):
            git_clone(BASE_HREF % arg)
            #thread?
        elif opt in ("-p", "--push"):
            git_push(arg)
        elif opt in ("-t", "--tags"):
            get_last_tag(arg)
            

if __name__ == "__main__":
    main(sys.argv[1:])
