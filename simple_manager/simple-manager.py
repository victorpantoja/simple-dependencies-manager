#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from simple_manager import __version__ as Version
from simple_manager.utils import git_clone

import sys
import subprocess
import yaml
import os

config = None
WORKSPACE = None
project = None

def get_last_tag():
    cmd = 'git describe --tags `git rev-list --tags --max-count=1`'
    cwd = '%s/%s'% (WORKSPACE, config['projects'][project]['name'])

    try:
        tag = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=cwd).stdout.read()
        print "Last tag for %s: %s" % (project, tag.replace("\n",""))
        return tag
    except:
        print "No tags found for %s" % project

def develop_install():
    cmd = ['python', 'setup.py', 'install', config['projects'][project]['repo']]
    p = subprocess.Popen(cmd, cwd=WORKSPACE)
    p.wait()

def git_update():
    print "Updating %s" % project
    cmd = ['git', 'pull']
    p = subprocess.Popen(cmd, cwd=WORKSPACE+'/'+config['projects'][project]['name'])
    p.wait()
    
def git_push():
    print "Sending changes of %s to remote server" % project
    cmd = ['git', 'push']
    p = subprocess.Popen(cmd, cwd=WORKSPACE+'/'+config['projects'][project]['name'])
    p.wait()

def git_push_tag():
    cmd = 'git push --tags'
    cwd = '%s/%s'% (WORKSPACE, config['projects'][project]['name'])
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=cwd).stdout.read()

def git_tag():
    git_update()
    tag = get_last_tag()

    new_tag = raw_input("Enter new tag: ")
    description = raw_input("Enter a description for this tag: ")

    cmd = 'git tag -a %s -m "%s"' % (new_tag, description)
    cwd = '%s/%s'% (WORKSPACE, config['projects'][project]['name'])

    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=cwd).stdout.read()
    
    git_push()
    git_push_tag()

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

    parser.add_option("-t", "--tag", action="store_true", dest="tag",
                      help="Tag a repo or all repos, if none tag is provided")

    parser.add_option("-r", "--repo", dest="project", metavar="(PROJECT|all)",
                      help="The project as configured in config.yaml")

    parser.add_option("-d", "--pip-develop", action="store_true", dest="develop",
                      help="Install dependencies in 'develop mode'")

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
            git_clone(project=project,
                      url=config['projects'][project]['repo'],
                      workspace=WORKSPACE)
        else:
            print "Cloning %s"  % ', '.join(config['projects'].keys())
            for repo in config['projects'].keys():
                git_clone(project=repo,
                          url=config['projects'][repo]['repo'],
                          workspace=WORKSPACE)

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
        else:
            print "Getting last tags for %s"  % ', '.join(config['projects'].keys())
            for repo in config['projects'].keys():
                project = repo
                get_last_tag()

    elif options.tag:
        if project != 'all':
            git_tag()
        else:
            print "Tagging projects %s"  % ', '.join(config['projects'].keys())
            for repo in config['projects'].keys():
                project = repo
                git_tag()

    elif options.develop:
        if project != 'all':
            develop_install()
        else:
            print "Installing projects %s"  % ', '.join(config['projects'].keys())
            for repo in config['projects'].keys():
                project = repo
                develop_install()

if __name__ == "__main__":
    main(sys.argv[1:])
