#!/usr/bin/python

from CoreFoundation import CFPreferencesSetValue, CFPreferencesSynchronize
from Foundation import NSDate
import subprocess


def set_value(key, value, domain):
    CFPreferencesSetValue(
        key, value, domain, "kCFPreferencesCurrentUser", "kCFPreferencesCurrentHost"
    )


def main():
    the_date = NSDate.date()
    set_value("doNotDisturb", True, "com.apple.notificationcenterui")
    set_value("doNotDisturbDate", the_date, "com.apple.notificationcenterui")
    CFPreferencesSynchronize(
        "com.apple.notificationcenterui",
        "kCFPreferencesCurrentUser",
        "kCFPreferencesAnyHost",
    )
    subprocess.call(["killall", "NotificationCenter"])


if __name__ == "__main__":
    main()
