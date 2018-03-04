import os, subprocess

def clone(repo, destination, branch=None):
    if not os.path.exists(destination):
        os.makedirs(destination)

    cmd = ["git", "clone"]
    if branch is not None:
        cmd += ["-b", branch, "--single-branch"]
    cmd += [repo, destination]
    subprocess.check_call(cmd)
