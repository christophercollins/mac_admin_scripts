#!/usr/bin/python

#!/usr/bin/python
# Copyright (C) 2015 Christopher Collins
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
#
# Plist parsing code from Greg Neagle http://www.github.com/gneagle

'''
hide_preference_panes.py

Hides all desired preference panes in System Preferences by editing
com.apple.systempreferences.plist for the currently logged in user.

Copy and paste into the PREFERENCE_PANES list any preference pane
identifiers you wish to hide. If you want to UNHIDE all preference panes,
make PREFERENCE_PANES an empty list.

3rd party preference pane identifiers can be found by reading Info.plist file
(e.g. /Library/PreferencePanes/JavaControlPanel.prefPane>/Info.plist), and making note
of the CFBundleIdentifier key. (e.g., the Java Control Panel'sCFBundleIdentifier key
is "com.oracle.java.JavaControlPanel")

The following is an extensive list of identifiers for preference panes shipped by Apple.

Personal:
com.apple.preference.general
com.apple.preference.desktopscreeneffect
com.apple.preference.dock
com.apple.preference.expose
com.apple.Localization
com.apple.preference.security
com.apple.preference.spotlight
com.apple.preference.notifications

Hardware:
com.apple.preference.digihub.discs
com.apple.preference.displays
com.apple.preference.energysaver
com.apple.preference.keyboard
com.apple.preference.mouse
com.apple.preference.trackpad
com.apple.preference.printfax
com.apple.preference.sound
com.apple.preference.ink
com.apple.preference.hardware
com.apple.prefpanel.fibrechannel

Networking:
com.apple.preferences.icloud
com.apple.preferences.internetaccounts
com.apple.preferences.extensions
com.apple.preference.internet
com.apple.preference.network
com.apple.preferences.Bluetooth
com.apple.preferences.sharing

System:
com.apple.preferences.users
com.apple.preferences.parentalcontrols
com.apple.preferences.appstore
com.apple.preference.speech
com.apple.preference.datetime
com.apple.preference.startupdisk
com.apple.prefs.backup
com.apple.preference.universalaccess
com.apple.preferences.configurationprofiles
com.apple.preference.xsan
'''

from Foundation import CFPreferencesCopyAppValue, NSData, NSPropertyListSerialization, NSPropertyListMutableContainers, NSPropertyListXMLFormat_v1_0
from SystemConfiguration import SCDynamicStoreCopyConsoleUser
from pwd import getpwnam
import sys
import os

# Globals
# Edit this list by adding the identifier for any preference panes you want to hide in System Preferences

PREFERENCE_PANES = ['com.apple.prefs.backup',
					'com.apple.preferences.icloud',
					'com.apple.preference.security',
					'com.apple.preferences.configurationprofiles']


class NSPropertyListSerializationException(Exception):
	pass


def readPlist(filepath):
	"""
	Read a .plist file from filepath.  Return the unpacked root object
	(which usually is a dictionary).
	"""
	plistData = NSData.dataWithContentsOfFile_(filepath)
	dataObject, plistFormat, error = NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(plistData, NSPropertyListMutableContainers, None, None)
	if error:
		errmsg = "%s in file %s" % (error, filepath)
		raise NSPropertyListSerializationException(errmsg)
	else:
		return dataObject


def writePlist(dataObject, filepath):
    '''
    Write 'rootObject' as a plist to filepath.
    '''
    plistData, error = NSPropertyListSerialization.dataFromPropertyList_format_errorDescription_(dataObject, NSPropertyListXMLFormat_v1_0, None)
    if error:
        raise NSPropertyListSerializationException(error)
    else:
        if plistData.writeToFile_atomically_(filepath, True):
            return
        else:
            raise Exception("Failed to write plist data to %s" % filepath)


def getCurrentUser():
	currentuser = (SCDynamicStoreCopyConsoleUser(None, None, None) or [None])[0]
	currentuser = [currentuser,""][currentuser in [u"loginwindow", None, u""]]
	return currentuser


def systemPreferencesPlistExists(currentuser):
	'''
	Check that com.apple.systempreferences.plist exists for the currently logged in user,
	and return the valid path, otherwise just print to screen and exit.
	'''
	pathtoplist = os.path.join('/Users/', currentuser, 'Library/Preferences/com.apple.systempreferences.plist')
	if os.path.exists(pathtoplist):
		return pathtoplist
	else:
		print "User {} doesn't have a plist.".format(currentuser)
		sys.exit()


def hidePreferencePanes(plist, preferencepanes):
	'''
	Add desired preference panes defined in global PREFERENCE_PANES list
	to 'HiddenPreferencePanes' array in com.applesystemprefences.plist.
	If PREFERENCE_PANES is empty, it will clear all hidden preference panes.
	'''
	# check if PREFERENCE_PANES is empty, and if it is,
	# clear out 'HiddenPreferencePanes' in plist
	if not preferencepanes:
		plist['HiddenPreferencePanes'] = []
		print "Unhiding all preference panes."
		return plist
	else:
		if not plist.has_key('HiddenPreferencePanes'):
			plist['HiddenPreferencePanes'] = []
		for pref in preferencepanes:
			if not pref in plist['HiddenPreferencePanes']:
				print "Hiding preference pane {}".format(pref)
				plist['HiddenPreferencePanes'].append(pref)
			else:
				print "Preference pane {} already hidden".format(pref)
		return plist


def fixPreferenceFilePermissions(filepath, currentuser):
	'''
	Set permissions on com.apple.systempreferences.plist file since script
	writes the file back to disk with root ownership.
	'''
	# get current user's uid as os.chown will not resolve usernames to uids
	useruid = getpwnam(currentuser).pw_uid
	os.chown(filepath, useruid, 20)


def main():
	'''
	Main function.
	'''
	currentuser = getCurrentUser()
	systempreferencesplist = systemPreferencesPlistExists(currentuser)
	parsed_plist = readPlist(systempreferencesplist)
	final_plist = hidePreferencePanes(parsed_plist, PREFERENCE_PANES)
	# Write the final modified plist
	writePlist(final_plist, systempreferencesplist)
	fixPreferenceFilePermissions(systempreferencesplist, currentuser)


if __name__ == "__main__":
	main()
