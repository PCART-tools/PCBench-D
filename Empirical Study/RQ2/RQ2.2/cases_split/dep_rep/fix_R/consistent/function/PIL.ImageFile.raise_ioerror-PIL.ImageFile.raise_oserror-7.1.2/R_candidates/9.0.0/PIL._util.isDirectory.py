def isDirectory(f):
    return isPath(f) and os.path.isdir(f)
