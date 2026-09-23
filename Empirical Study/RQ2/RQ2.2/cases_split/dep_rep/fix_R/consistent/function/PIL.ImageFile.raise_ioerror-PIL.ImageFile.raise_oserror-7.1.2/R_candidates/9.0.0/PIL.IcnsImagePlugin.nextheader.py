def nextheader(fobj):
    return struct.unpack(">4sI", fobj.read(HEADERSIZE))
