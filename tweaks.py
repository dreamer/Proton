#!/usr/bin/env python3

"""
This module lists game-specific tweaks, that cannot be handled by other means
(specifically tweaks, that are outside of dxvk.conf or Mesa scope, such as
additional environment variables, renaming files post-installation, changing
Wine settings for the specific game, etc.).  The purpose is similar to
"Install Scripts" *.vfd files distributed with games, except here tweaks are
provided by Proton community and not game developer.
"""

import os
import re
import shutil
import subprocess
import sys


TWEAKS_DB = {
    # Call of Duty® (2003)
    '2620': {
        'env': {
            'MESA_EXTENSION_MAX_YEAR': '2003',
            '__GL_ExtensionStringVersion': '17700',
        }
    },
    # STAR WARS™ Jedi Knight - Jedi Academy™
    '6020': {
        'env': {
            'MESA_EXTENSION_MAX_YEAR': '2003',
            '__GL_ExtensionStringVersion': '17700',
        }
    },
    # STAR WARS™ Jedi Knight II - Jedi Outcast™
    '6030': {
        'env': {
            'MESA_EXTENSION_MAX_YEAR': '2003',
            '__GL_ExtensionStringVersion': '17700',
        },
        'commands': {
            r'.*jk2sp.exe$': ['+r_ignorehwgamma', '1'],
            r'.*jk2mp.exe$': ['+r_ignorehwgamma', '1'],
        }
    },
}


class Tweaks:  # pylint: disable=too-few-public-methods
    """
    Class grouping tweaks for a specific game
    """

    def __init__(self, appid):
        self.prefix = os.environ['STEAM_COMPAT_DATA_PATH'] + '/pfx/'
        self.env = {}
        self.commands = {}
        if os.environ.get('PROTON_NO_TWEAKS') == '1':
            return
        if appid in TWEAKS_DB:
            self.env = TWEAKS_DB[appid].get('env') or {}
            self.commands = TWEAKS_DB[appid].get('commands') or {}


    def modify_command(self, args):
        """Add commandline parameters defined for this app

        If user decides to modify 'Set launch options' and append some args,
        then it will override whatever is defined in TWEAKS_DB.

        Games can provide multiple binaries, each binary can have
        separate list of tweaked commandline args.
        """
        cmd = args[-1]
        for expr, extra_args in self.commands.items():
            exe_pattern = re.compile(expr)
            if exe_pattern.match(cmd):
                return args + extra_args
        return args
