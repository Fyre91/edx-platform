import sys
import os
sys.path.append(os.path.abspath('.'))

from paver.easy import task, needs, consume_args, no_help
from subprocess import call
from pprint import pprint

from pavements.config import config
from pavements.helpers import *
import pavements.docs
from pavements.prereqs import *


@task
# default does not automatically run auto, unlike other tasks
@needs(['auto'])
def default():
    """ Default task - run test, pep8, pylint. """
    pass_to_rake(['test', 'pep8', 'pylint'])


@task
@no_help
def auto():
    """ Setup for other tasks """
    pass


@task
def print_config():
    """ Print paver config """
    pprint(config)


@task
@consume_args
def rake(args):
    """ Forward commands to rake. """
    pass_to_rake(args)


def pass_to_rake(args):
    print "passing through to rake with args: %s" % str(args)
    call(["rake"] + args)
