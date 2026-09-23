def chunks(chunkable, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(chunkable), n):
        yield chunkable[i: i + n]
