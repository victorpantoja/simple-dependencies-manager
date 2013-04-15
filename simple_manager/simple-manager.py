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
        opts, args = getopt.getopt(argv,"hy:r:ucpTt:",["update=","create=","push=","tags=","yaml="])
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

            if not config['projects'].get(project):
                print "Project '%s' is not configured in config.yaml. Please, verify." % project
            sys.exit(2)

        elif opt in ("-u", "--update"):
            git_update()

        elif opt in ("-c", "--create"):
            git_clone()
            #thread?

        elif opt in ("-p", "--push"):
            git_push()

        elif opt in ("-T", "--tags"):
            get_last_tag()
            
        elif opt in ("-t", "--tag"):
            if project == 'all':
                print "You must specify only one project to use -t option but you specified 'all'"
                sys.exit(2)
            else:
                tag = arg
                git_tag()
            

if __name__ == "__main__":
    main(sys.argv[1:])
