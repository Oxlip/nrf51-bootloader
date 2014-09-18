#!/bin/env python2.7

import re
import git

repo = git.Repo('.')
assert repo.bare == False

if repo.head.reference.name != 'master':
    version = '0x00000000'
else:
    tag = None
    for tagref in repo.tags:
        if tagref.commit == repo.head.reference.commit:
            tag = tagref.name
            break
    if tag is None:
        print 'Can\' get the version to build this release'

    m = re.match(r'v(?P<major>\d+).(?P<minor>\d+).(?P<bugfix>\d+)', tag)
    if m is None:
        print 'Can\' get the version to build this release'
    version  = (int(m.group('major')) << 24)
    version += (int(m.group('minor')) << 12)
    version +=  int(m.group('bugfix'))
    version = hex(version)

with open('include/version.h', 'a') as f:
    f.write('#ifndef VERSION_H_\n')
    f.write('#define VERSION_H_\n\n')
    f.write('#define BOOTLOADER_VERSION {}\n\n'.format(version))
    f.write('#endif // VERSION_H_\n')

