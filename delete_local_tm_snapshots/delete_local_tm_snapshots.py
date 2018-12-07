#!/usr/bin/python

##	Script:		delete_local_tm_snapshots.py
##	Author:		Christopher Collins badlittlerobots@gmail.com
##	Last Change:	2018-12-07
###########################################
##  Description: Simple script to purge all local time machine snapshots.
###########################################

# Copyright (C) 2018 Christopher Collins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess

def get_local_snapshots():
    cmd = ['tmutil', 'listlocalsnapshots', '/']
    result = subprocess.check_output(cmd)
    return [ x.split('com.apple.TimeMachine.')[1] for x in result.splitlines() ]

def delete_local_snapshots(snapshots):
    if snapshots:
        length = len(snapshots)
        count = 1
        for snapshot in snapshots:
            cmd = ['tmutil', 'deletelocalsnapshots', snapshot]
            print("Deleting local snapshot {} ({}/{})".format(snapshot, count, length))
            count += 1
            subprocess.call(cmd)
    else:
        print("No snapshots to delete.")

def main():
    snapshots = get_local_snapshots()
    delete_local_snapshots(snapshots)

if __name__ == '__main__':
    main()