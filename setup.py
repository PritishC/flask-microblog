#!/home/pritishc/.virtualenvs/flaskhost/bin/python
import os, subprocess, sys
#subprocess.call(['python', 'virtualenv.py', 'flask'])
if sys.platform == 'win32':
    bin = 'Scripts'
else:
    bin = 'bin'
subprocess.call('pip', 'install', 'flask<0.10')
subprocess.call('pip', 'install', 'flask-login')
subprocess.call('pip', 'install', 'flask-openid')
if sys.platform == 'win32':
    subprocess.call('pip', 'install', '--no-deps', 'lamson', 'chardet', 'flask-mail')
else:
    subprocess.call('pip', 'install', 'flask-mail')
subprocess.call('pip', 'install', 'sqlalchemy==0.7.9')
subprocess.call('pip', 'install', 'flask-sqlalchemy')
subprocess.call('pip', 'install', 'sqlalchemy-migrate')
#subprocess.call('pip', 'install', 'flask-whooshalchemy'])
subprocess.call('pip', 'install', 'git+git://github.com/miguelgrinberg/Flask-WhooshAlchemy')
subprocess.call('pip', 'install', 'flask-wtf')
subprocess.call('pip', 'install', 'flask-babel')
subprocess.call('pip', 'install', 'guess-language')
subprocess.call('pip', 'install', 'flup')
subprocess.call('pip', 'install', 'coverage')
