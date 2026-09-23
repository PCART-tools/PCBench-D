def deleteDirectory(top_dir):
    for root, dirs, files in os.walk(top_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top_dir)
