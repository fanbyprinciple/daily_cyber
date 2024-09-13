import os
import datetime

x= datetime.datetime.now()

text = "push on"

os.system('cmd /c "git add ."')
os.system(f'cmd /c "git commit -m \"{text} {x}\"')
os.system('cmd /c "git push"')


