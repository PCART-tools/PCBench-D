    def _local_timestamps(self):
        if self.is_monotonic:
            return conversion.tz_convert(self.asi8, utc, self.tz)
        else:
            values = self.asi8
            indexer = values.argsort()
            result = conversion.tz_convert(values.take(indexer), utc, self.tz)

            n = len(indexer)
            reverse = np.empty(n, dtype=np.int_)
            reverse.put(indexer, np.arange(n))
            return result.take(reverse)
