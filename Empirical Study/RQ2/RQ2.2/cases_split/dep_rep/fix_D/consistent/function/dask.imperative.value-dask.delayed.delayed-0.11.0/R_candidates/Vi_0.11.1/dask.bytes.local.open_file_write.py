def open_file_write(paths):
    """ Open list of files using delayed """
    out = [delayed(open)(path, 'wb') for path in paths]
    return out
