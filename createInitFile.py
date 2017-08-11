#!/usr/bin/env python
"""Writes the current version, build platform etc to
"""
from __future__ import print_function
from past.builtins import str
import os, copy, platform, subprocess
thisLoc = os.path.split(__file__)[0]

def createInitFile(dist=None, version=None, sha=None):
    """Write the version file to psychopy/version.py

    :param:`dist` can be:
        None:
            writes __version__
        'sdist':
            for python setup.py sdist - writes __version__ and git id (__git_sha__)
        'bdist':
            for python setup.py bdist - writes __version__, git id (__git_sha__)
            and __build_platform__
    """
    #get default values if None
    if version is None:
        with open(os.path.join(thisLoc,'version')) as f:
            version = f.read()
            version = version.replace("\n", "")
    if sha is None:
        sha = _getGitShaString(dist)
    platformStr = _getPlatformString(dist)

    infoDict = {'version' : version,
                'shaStr' : sha,
                'platform' : platformStr,
                }
    #write it
    with open(os.path.join(thisLoc, 'psychopy','__init__.py'), 'w') as f:
        outStr = template.format(**infoDict)
        f.write(outStr)
    print('wrote init for', version, sha)
    #and return it
    return outStr

template="""# Part of the PsychoPy library
# Copyright (C) 2015 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).

# --------------------------------------------------------------------------
# This file is automatically generated during build (do not edit directly).
# --------------------------------------------------------------------------

import os
import sys

# version info for PsychoPy
__version__ = '{version}'
__license__ = 'GNU GPLv3 (or more recent equivalent)'
__author__ = 'Jonathan Peirce'
__author_email__ = 'jon@peirce.org.uk'
__maintainer_email__ = 'psychopy-dev@googlegroups.com'
__users_email__ = 'psychopy-users@googlegroups.com'
__url__ = 'http://www.psychopy.org'
__downloadUrl__ = 'https://github.com/psychopy/psychopy/releases/'
__git_sha__ = '{shaStr}'
__build_platform__ = '{platform}'

__all__ = ["gui", "misc", "visual", "core",
           "event", "data", "sound", "microphone"]

# for developers the following allows access to the current git sha from
# their repository
if __git_sha__ == 'n/a':
    import subprocess
    # see if we're in a git repo and fetch from there
    try:
        thisFileLoc = os.path.split(__file__)[0]
        output = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'],
                                         cwd=thisFileLoc, stderr=subprocess.PIPE)
    except Exception:
        output = False
    if output:
        __git_sha__ = output.strip()  # remove final linefeed

# update preferences and the user paths
from psychopy.preferences import prefs
for pathName in prefs.general['paths']:
    sys.path.append(pathName)

from psychopy.tools.versionchooser import useVersion, ensureMinimal
"""

def _getGitShaString(dist=None, sha=None):
    """If generic==True then returns empty __git_sha__ string
    """
    shaStr='n/a'
    if dist is not None:
        proc = subprocess.Popen('git rev-parse --short HEAD',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd='.', shell=True)
        repo_commit, _ = proc.communicate()
        del proc#to get rid of the background process
        if repo_commit:
            shaStr=str(repo_commit.strip())#remove final linefeed
        else:
            shaStr='n/a'
        #this looks neater but raises errors on win32
        #        output = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).split()[0]
        #        if output:
        #            shaStr = output
    return shaStr

def _getPlatformString(dist=None):
    """If generic==True then returns empty __build_platform__ string
    """
    if dist=='bdist':
        #get platform-specific info
        if os.sys.platform=='darwin':
            OSXver, junk, architecture = platform.mac_ver()
            systemInfo = "OSX_%s_%s" %(OSXver, architecture)
        elif os.sys.platform=='linux':
            systemInfo = '%s_%s_%s' % (
                'Linux',
                ':'.join([x for x in platform.dist() if x != '']),
                platform.release())
        elif os.sys.platform=='win32':
            ver=os.sys.getwindowsversion()
            if len(ver[4])>0:
                systemInfo="win32_v%i.%i.%i (%s)" %(ver[0],ver[1],ver[2],ver[4])
            else:
                systemInfo="win32_v%i.%i.%i" %(ver[0],ver[1],ver[2])
        else:
            systemInfo = platform.system()+platform.release()
    else:
        systemInfo="n/a"
    return systemInfo

if __name__=="__main__":
    createInitFile()
