import os, sys

os.system("python ./interpolate.py")
os.system("python ./dbscan.py ./snapshot/ ./clusters/")
os.system("python ./intersect.py")
os.system("python ./showLinePattern.py")
