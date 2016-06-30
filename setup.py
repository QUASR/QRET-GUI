# Py2exe wrapper
# Converts python file to windows executable

from distutils.core import setup
import py2exe

setup(console=['QRET_GUI.py'])
input("Press enter to exit")
