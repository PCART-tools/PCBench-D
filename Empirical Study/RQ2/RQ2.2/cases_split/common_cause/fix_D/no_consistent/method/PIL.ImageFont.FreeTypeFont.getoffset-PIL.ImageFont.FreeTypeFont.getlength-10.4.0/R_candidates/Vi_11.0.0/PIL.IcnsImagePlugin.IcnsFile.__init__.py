    def __init__(self, fobj: IO[bytes]) -> None:
        """
        fobj is a file-like object as an icns resource
        """
        # signature : (start, length)
        self.dct = {}
        self.fobj = fobj
        sig, filesize = nextheader(fobj)
        if not _accept(sig):
            msg = "not an icns file"
            raise SyntaxError(msg)
        i = HEADERSIZE
        while i < filesize:
            sig, blocksize = nextheader(fobj)
            if blocksize <= 0:
                msg = "invalid block header"
                raise SyntaxError(msg)
            i += HEADERSIZE
            blocksize -= HEADERSIZE
            self.dct[sig] = (i, blocksize)
            fobj.seek(blocksize, io.SEEK_CUR)
            i += blocksize
