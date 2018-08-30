from distutils.core import setup

setup(name='indicator-prayer-times',
      version='0.31',
      description='A Prayer Times displayer for Indicator Applet.',
      author='indicator-prayer-times developers',
      py_modules=['prayertime','HijriCal','hijra','configer','handler'],
      scripts=['indicator-prayer-times'],
      data_files=[('/usr/share/icons/hicolor/scalable/apps',['icons/indicator-prayer-times.svg']),
                  ('/usr/share/applications',['indicator-prayer-times.desktop']),
                  ('/etc/xdg/autostart', ['indicator-prayer-times.desktop'])]
      )
