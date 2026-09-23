def infer_compression(filename):
    extension = os.path.splitext(filename)[-1].strip('.')
    return compressions.get(extension, None)
