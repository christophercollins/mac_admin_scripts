# `hide_preference_panes.py`

##Intro:
This script was created when a fellow Mac admin was using configuration profiles to lock down preference panes in System Preferences but did not want the user to see the greyed out preference panes.

This can be accomplished manually in System Preferences by holding the "show all" button until you trigger the popup menu which you can then scroll down to the bottom of the list and choose "customize".

This script is intended to be able to set these preferences in a automated and repeatable fashion via a management system (e.g. Casper, etc.)

##Basic usage:

The script gets the current logged in user and adds the preference panes you wish to be hidden to their com.apple.systempreferences.plist file. It double checks to make sure that each preference pane is not already hidden.

You should edit the variable named **PREFERENCE_PANES** and add your desired preference pane identifiers for preference panes you wish to hide. There is a list of all the built-in Apple preference panes in the comments of the script for convenience. If you need to know how to access 3rd party preference panes, those instructions are also in the script.

If you want to clear out all hidden identifiers and return the user's preferences back to their default then you should make **PREFERENCE_PANES** empty. This will make the script clear those out.

