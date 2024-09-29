import os
import datetime

x= datetime.datetime.now()

how_many_commits = 3 # commits 7 days before today
text = "push on"
# commit_file = open("commit.txt", "w")
# os.system('cmd /c "git add ."')
i = 4
j = i
while(i < j + how_many_commits):
    with open("commit_file", "w") as commit_file:
        commit_file.write(str(i))
    os.system('cmd /c "git add ."')
    os.system(f'cmd /c "git commit -m \"{text} {x}\" --date=\"{i} days ago\"')
    i += 1
os.system('cmd /c "git push"')



