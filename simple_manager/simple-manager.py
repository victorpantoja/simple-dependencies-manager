#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import subprocess
import yaml
import os

config = None
WORKSPACE = None

def get_last_tag(repo):
    cmd = 'git describe --tags `git rev-list --tags --max-count=1`'
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
    global config
    global WORKSPACE

    try:
        opts, args = getopt.getopt(argv,"hy:u:c:p:t",["update=","create=","push=","tags=","yaml="])
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
            git_clone(WORKSPACE % arg)
            #thread?
        elif opt in ("-p", "--push"):
            git_push(arg)
        elif opt in ("-t", "--tags"):
            get_last_tag(arg)
        elif opt in ("-y", "--yaml"):
            config = yaml.load(open(arg, 'r'))
            WORKSPACE = config['workspace']
            print WORKSPACE
            

if __name__ == "__main__":
    main(sys.argv[1:])
