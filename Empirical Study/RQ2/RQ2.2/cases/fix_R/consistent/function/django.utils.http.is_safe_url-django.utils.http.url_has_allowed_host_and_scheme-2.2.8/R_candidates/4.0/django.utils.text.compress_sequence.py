def compress_sequence(sequence):
    buf = StreamingBuffer()
    with GzipFile(mode='wb', compresslevel=6, fileobj=buf, mtime=0) as zfile:
        # Output headers...
        yield buf.read()
        for item in sequence:
            zfile.write(item)
            data = buf.read()
            if data:
                yield data
    yield buf.read()
