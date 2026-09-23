def textblock(filename, start, end, compression=None, encoding=system_encoding,
              linesep=os.linesep, buffersize=4096):
    """Pull out a block of text from a file given start and stop bytes.

    This gets data starting/ending from the next linesep delimiter. Each block
    consists of bytes in the range [start,end[, i.e. the stop byte is excluded.
    If `start` is 0, then `start` corresponds to the true start byte. If
    `start` is greater than 0 and does not point to the beginning of a new
    line, then `start` is incremented until it corresponds to the start byte of
    the next line. If `end` does not point to the beginning of a new line, then
    the line that begins before `end` is included in the block although its
    last byte exceeds `end`.

    Examples
    --------
    >> with open('myfile.txt', 'wb') as f:
    ..     f.write('123\n456\n789\nabc')

    In the example below, 1 and 10 don't line up with endlines.

    >> u''.join(textblock('myfile.txt', 1, 10))
    '456\n789\n'
    """
    # Make sure `linesep` is not a byte string because
    # `io.TextIOWrapper` in Python versions other than 2.7 dislike byte
    # strings for the `newline` argument.
    linesep = str(linesep)

    # Get byte representation of the line separator.
    bin_linesep = get_bin_linesep(encoding, linesep)
    bin_linesep_len = len(bin_linesep)

    if buffersize < bin_linesep_len:
        error = ('`buffersize` ({0:d}) must be at least as large as the '
                 'number of line separator bytes ({1:d}).')
        raise ValueError(error.format(buffersize, bin_linesep_len))

    chunksize = end - start

    with open(filename, 'rb', compression) as f:
        with io.BufferedReader(f) as fb:
            # If `start` does not correspond to the beginning of the file, we
            # need to move the file pointer to `start - len(bin_linesep)`,
            # search for the position of the next a line separator, and set
            # `start` to the position after that line separator.
            if start > 0:
                # `start` is decremented by `len(bin_linesep)` to detect the
                # case where the original `start` value corresponds to the
                # beginning of a line.
                start = max(0, start - bin_linesep_len)
                # Set the file pointer to `start`.
                fb.seek(start)
                # Number of bytes to shift the file pointer before reading a
                # new chunk to make sure that a multi-byte line separator, that
                # is split by the chunk reader, is still detected.
                shift = 1 - bin_linesep_len
                while True:
                    buf = f.read(buffersize)
                    if len(buf) < bin_linesep_len:
                        raise StopIteration
                    try:
                        # Find the position of the next line separator and add
                        # `len(bin_linesep)` which yields the position of the
                        # first byte of the next line.
                        start += buf.index(bin_linesep)
                        start += bin_linesep_len
                    except ValueError:
                        # No line separator was found in the current chunk.
                        # Before reading the next chunk, we move the file
                        # pointer back `len(bin_linesep) - 1` bytes to make
                        # sure that a multi-byte line separator, that may have
                        # been split by the chunk reader, is still detected.
                        start += len(buf)
                        start += shift
                        fb.seek(shift, os.SEEK_CUR)
                    else:
                        # We have found the next line separator, so we need to
                        # set the file pointer to the first byte of the next
                        # line.
                        fb.seek(start)
                        break

            with io.TextIOWrapper(fb, encoding, newline=linesep) as fbw:
                # Retrieve and yield lines until the file pointer reaches
                # `end`.
                while start < end:
                    line = next(fbw)
                    # We need to encode the line again to get the byte length
                    # in order to correctly update `start`.
                    bin_line_len = len(line.encode(encoding))
                    if chunksize < bin_line_len:
                        error = ('`chunksize` ({0:d}) is less than the line '
                                 'length ({1:d}). This may cause duplicate '
                                 'processing of this line. It is advised to '
                                 'increase `chunksize`.')
                        raise IOError(error.format(chunksize, bin_line_len))

                    yield line
                    start += bin_line_len
