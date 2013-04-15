#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from simple_manager import __version__ as Version

import sys
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
    p = subprocess.Popen(cmd, cwd=WORKSPACE+'/'+config['projects'][project]['name'])
    p.wait()
    
def git_push():
    cmd = ['git', 'push']
    p = subprocess.Popen(cmd, cwd=WORKSPACE+'/'+config['projects'][project]['name'])
    p.wait()

def main(argv):
    global config
    global yaml_file
    global WORKSPACE
    global project

    parser = OptionParser(version=Version)
    parser.add_option("-c", "--clone", action="store_true", dest="clone",
                      help="Clone a project")

    parser.add_option("-f", "--file", dest="filename", help="Path do config.yaml",
                      metavar="FILE")

    parser.add_option("-p", "--push", action="store_true", dest="push",
                      help="Push changes to remote repository")

    parser.add_option("-u", "--update", action="store_true", dest="update", help="Update repositories.")

    parser.add_option("-T", "--TAGS", action="store_true", dest="tags",
                      help="Show last tags por all configured repositories")

    parser.add_option("-t", "--tag", dest="tag",
                      help="Tag a repo or all repos, if none tag is provided")

    parser.add_option("-r", "--repo", dest="project", metavar="(PROJECT|all)",
                      help="The project as configured in config.yaml")

    (options, args) = parser.parse_args()

    if not options.filename:
        print 'You must provide a config.yaml file.'
        sys.exit(2)
    
    yaml_file = options.filename
    config = yaml.load(open(yaml_file, 'r'))
    WORKSPACE = config['workspace']
    
    if options.project:
        project = options.project
        if not config['projects'].get(options.project):
            print "Project '%s' is not configured in config.yaml. Please, verify." % project
            sys.exit(2)
    else:
        project = "all"

    if options.update:
        if project != 'all':
            git_update()
        else:
            print "Updating %s"  % ', '.join(config['projects'].keys())
            for repo in config['projects'].keys():
                project = repo
                git_update()

    elif options.clone:
        if project != 'all':
            git_clone()
        else:
            print "Cloning %s"  % ', '.join(config['projects'].keys())
            for repo in config['projects'].keys():
                project = repo
                git_clone()

    elif options.push:
        if project != 'all':
            git_push()
        else:
            print "Pushing %s"  % ', '.join(config['projects'].keys())
            for repo in config['projects'].keys():
                project = repo
                git_push()

    elif options.tags:
        if project != 'all':
            get_last_tag()
            print "Getting lasts tags for %s"  % ', '.join(config['projects'].keys())
            for repo in config['projects'].keys():
                project = repo
                get_last_tag()

    elif options.tag:
        if project == 'all':
            git_tag()
        else:
            print "Tagging projects %s"  % ', '.join(config['projects'].keys())
            #print "User you be promped to enter each desired tag"
            for repo in config['projects'].keys():
                git_tag()


if __name__ == "__main__":
    main(sys.argv[1:])
