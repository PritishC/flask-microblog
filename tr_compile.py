#!/home/pritishc/Envs/ircflask/bin/python
__author__ = 'pritishc'

import os
import sys
if sys.platform == 'win32':
    pybabel = 'flask\\Scripts\\pybabel'
else:
    pybabel = 'pybabel'
os.system(pybabel + ' compile -d app/translations')