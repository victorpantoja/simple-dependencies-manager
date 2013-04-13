#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import subprocess
import yaml
import os

config = None
WORKSPACE = None
project = None

def get_last_tag():
    cmd = 'git describe --tags `git rev-list --tags --max-count=1`'
    p = subprocess.Popen(cmd, cwd=WORKSPACE+'/'+project)
    p.wait()

def git_clone():
    cmd = ['git', 'clone', config['projects'][project]['repo']]
    print "Cloning %s into %s" % (project, WORKSPACE)
    p = subprocess.Popen(cmd, cwd=WORKSPACE)
    p.wait()

def git_update():
    cmd = ['git', 'pull']
    p = subprocess.Popen(cmd, cwd=WORKSPACE+'/'+project)
    p.wait()
    
def git_push():
    cmd = ['git', 'push']
    p = subprocess.Popen(cmd, cwd=WORKSPACE+'/'+project)
    p.wait()

def main(argv):
    global config
    global yaml_file
    global WORKSPACE
    global project

    try:
        opts, args = getopt.getopt(argv,"hy:r:ucpt",["update=","create=","push=","tags=","yaml="])
    except getopt.GetoptError:
        print 'Usage: python simple-manager -y <yaml file> -c <project> -[cptu]'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'python simple-manager -y <yaml file> -c <project> -[cptu]'
            sys.exit()

        elif opt in ("-y", "--yaml"):
            yaml_file = arg
            config = yaml.load(open(yaml_file, 'r'))
            WORKSPACE = config['workspace']

        elif opt in ("-r", "--repo"):
            project = arg

        elif opt in ("-u", "--update"):
            git_update()

        elif opt in ("-c", "--create"):
            git_clone()
            #thread?

        elif opt in ("-p", "--push"):
            git_push()

        elif opt in ("-t", "--tags"):
            get_last_tag()
            

if __name__ == "__main__":
    main(sys.argv[1:])
