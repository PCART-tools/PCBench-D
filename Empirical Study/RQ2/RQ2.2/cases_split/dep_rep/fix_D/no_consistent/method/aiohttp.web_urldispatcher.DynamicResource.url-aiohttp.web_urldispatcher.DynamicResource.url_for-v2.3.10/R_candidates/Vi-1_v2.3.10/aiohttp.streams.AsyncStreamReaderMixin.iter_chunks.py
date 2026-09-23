        def iter_chunks(self):
            """Returns an asynchronous iterator that yields chunks of data
            as they are received by the server. The yielded objects are tuples
            of (bytes, bool) as returned by the StreamReader.readchunk method.

            Python-3.5 available for Python 3.5+ only
            """
            return ChunkTupleAsyncStreamIterator(self.readchunk)
