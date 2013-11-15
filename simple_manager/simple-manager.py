#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from simple_manager import __version__ as Version
from simple_manager.utils import git_clone
from simple_manager.utils import git_push
from simple_manager.utils import git_push_tag
from simple_manager.utils import git_update
from simple_manager.utils import git_status
from simple_manager.utils import get_last_tag

import sys
import subprocess
import yaml
import os

config = None
WORKSPACE = None
project = None

def develop_install():
    cmd = ['python', 'setup.py', 'install', config['projects'][project]['repo']]
    p = subprocess.Popen(cmd, cwd=WORKSPACE)
    p.wait()

# def git_tag():
#     git_update(WORKSPACE, config['projects'][project]['name'])
#     tag = get_last_tag()
# 
#     new_tag = raw_input("Enter new tag: ")
#     description = raw_input("Enter a description for this tag: ")
# 
#     cmd = 'git tag -a %s -m "%s"' % (new_tag, description)
#     cwd = '%s/%s'% (WORKSPACE, config['projects'][project]['name'])
# 
#     subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, cwd=cwd).stdout.read()
#     
#     git_push(WORKSPACE, config['projects'][project]['name'])
#     git_push_tag(WORKSPACE, config['projects'][project]['name'])

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

    parser.add_option("-s", "--status", action="store_true", dest="status", help="See repositories statuses.")

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
            git_update(WORKSPACE, project)
        else:
            for repo in config['projects'].keys():
                project = repo
                git_update(WORKSPACE, project)

    if options.status:
        if project != 'all':
            git_status(WORKSPACE, project)
        else:
            for repo in config['projects'].keys():
                project = repo
                git_status(WORKSPACE, project)

    if options.clone:
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
            git_push(WORKSPACE, config['projects'][project]['name'])
        else:
            print "Pushing %s"  % ', '.join(config['projects'].keys())
            for repo in config['projects'].keys():
                project = repo
                git_push()

    elif options.tags:
        if project != 'all':
            get_last_tag(WORKSPACE, project)
        else:
            print "Getting last tags for %s"  % ', '.join(config['projects'].keys())
            for repo in config['projects'].keys():
                project = repo
                get_last_tag(WORKSPACE, project)

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
