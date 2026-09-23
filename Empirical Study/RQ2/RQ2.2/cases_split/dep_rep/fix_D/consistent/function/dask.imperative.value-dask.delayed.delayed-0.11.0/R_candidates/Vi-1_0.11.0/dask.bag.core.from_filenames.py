def from_filenames(filenames, chunkbytes=None, compression='infer',
                   encoding=system_encoding, linesep=os.linesep):
    """ Deprecated.  See read_text """
    warn("db.from_filenames is deprecated in favor of db.read_text")
    from .text import read_text
    return read_text(filenames, blocksize=chunkbytes, compression=compression,
            encoding=encoding, linedelimiter=linesep)
