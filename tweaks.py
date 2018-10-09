#!/usr/bin/env python3

"""
This module lists game-specific tweaks, that cannot be handled by other means
(specifically tweaks, that are outside of dxvk.conf or Mesa scope, such as
additional environment variables, renaming files post-installation, changing
Wine settings for the specific game, etc.).  The purpose is similar to
"Install Scripts" *.vfd files distributed with games, except here tweaks are
provided by Proton community and not game developer.
"""

import configparser
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
    # Return to Castle Wolfenstein
    '9010': {
        'env': {
            'MESA_EXTENSION_MAX_YEAR': '2003',
            '__GL_ExtensionStringVersion': '17700',
        }
    },
    # Tomb Raider I
    '224960': {
        'conf_file': 'glide_fix.conf',
        'conf_dict': {'glide': {'glide': 'emu'}},
        'commands': {
            r'.*dosbox.exe$': ['-conf', 'glide_fix.conf'],
        }
    },
}


class Tweaks:  # pylint: disable=too-few-public-methods
    """
    Class grouping tweaks for a specific game
    """

    def __init__(self, appid):
        self.prefix = os.path.join(os.environ['STEAM_COMPAT_DATA_PATH'], 'pfx')
        self.env = {}
        self.commands = {}
        self.conf_file = ''
        self.conf_dict = {}
        if os.environ.get('PROTON_NO_TWEAKS') == '1':
            return
        if appid in TWEAKS_DB:
            for name, value in TWEAKS_DB[appid].items():
                self.__dict__[name] = value or self.__dict__[name]


    def needs_config(self):  # pylint: disable=missing-docstring
        exists = lambda: os.access(self.conf_file, os.F_OK)
        return self.conf_file and self.conf_dict and not exists()


    def create_config(self):
        """Create configuration file in ini format
        """
        conf = configparser.ConfigParser()
        conf.read_dict(self.conf_dict)
        with open(self.conf_file, 'w') as file:
            conf.write(file)


    def modify_command(self, args):
        """Add commandline parameters defined for this app

        If user decides to modify 'Set launch options' and append some args,
        then it will override whatever is defined in TWEAKS_DB.

        Games can provide multiple binaries, each binary can have
        separate list of tweaked commandline args.
        """
        for expr, extra_args in self.commands.items():
            exe_pattern = re.compile(expr)
            if any(exe_pattern.match(arg) for arg in args):
                return args + extra_args
        return args
