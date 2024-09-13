import os
import datetime

x= datetime.datetime.now()

how_many_commits = 7 # commits 7 days before today
text = "push on"
# commit_file = open("commit.txt", "w")
# os.system('cmd /c "git add ."')
i = 1
while(i < 7):
    with open("commit_file", "w") as commit_file:
        commit_file.write(str(i))
    os.system('cmd /c "git add ."')
    os.system(f'cmd /c "git commit -m \"{text} {x}\" --date=\"{i} days ago\"')

os.system('cmd /c "git push"')



