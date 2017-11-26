import os


def sys_path_append(dir):
    os.environ["PATH"] += os.pathsep + dir
