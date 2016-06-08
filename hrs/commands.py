# -*- coding: utf-8 -*-

"""
    hrs.commands
    ~~~~~~~~~~~~
"""

import sys

from flask_script import Manager, Command, prompt_bool
from flask_script.commands import ShowUrls

from hrs.application import create_app
from hrs.models import db


manager = Manager(create_app)


@manager.command
def initdb():
    db.create_all()


@manager.command
def dropdb():
    if prompt_bool("Are you sure ? You will lose all your data!"):
        db.drop_all()

manager.add_command("show-urls", ShowUrls())


class PyTest(Command):
    "Run py.test over the entire project"

    def run(self):
        try:
            import pytest
        except ImportError:
            sys.exit("You must have installed py.test to run this command")
        errno = pytest.main(sys.argv[2:])
        sys.exit(errno)

manager.add_command("test", PyTest())


def main():
    manager.run()
