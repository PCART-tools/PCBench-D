def getName(filePath):
    return os.path.basename(filePath).replace("/", "_").replace(".", "_")
