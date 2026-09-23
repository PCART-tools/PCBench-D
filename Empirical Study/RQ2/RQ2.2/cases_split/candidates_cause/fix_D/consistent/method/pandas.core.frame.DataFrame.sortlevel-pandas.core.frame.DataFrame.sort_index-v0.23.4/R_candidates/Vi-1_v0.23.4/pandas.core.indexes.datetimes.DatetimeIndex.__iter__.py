    def __iter__(self):
        """
        Return an iterator over the boxed values

        Returns
        -------
        Timestamps : ndarray
        """

        # convert in chunks of 10k for efficiency
        data = self.asi8
        length = len(self)
        chunksize = 10000
        chunks = int(length / chunksize) + 1
        for i in range(chunks):
            start_i = i * chunksize
            end_i = min((i + 1) * chunksize, length)
            converted = libts.ints_to_pydatetime(data[start_i:end_i],
                                                 tz=self.tz, freq=self.freq,
                                                 box="timestamp")
            for v in converted:
                yield v
