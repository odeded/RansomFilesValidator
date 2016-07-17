import os

ROOT_FOLDER = r"c:\kivy"
print "oded"
for root, dirs, files in os.walk(ROOT_FOLDER):
    for file in files:
    #    if file.endswith(".txt"):
        print(os.path.join(root, file))