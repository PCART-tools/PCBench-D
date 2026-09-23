def dump_dataset(filename, data):
    fid = open(filename, 'w')
    try:
        for line in data:
            fid.write("%s\n" % " ".join(line))
    finally:
        fid.close()
