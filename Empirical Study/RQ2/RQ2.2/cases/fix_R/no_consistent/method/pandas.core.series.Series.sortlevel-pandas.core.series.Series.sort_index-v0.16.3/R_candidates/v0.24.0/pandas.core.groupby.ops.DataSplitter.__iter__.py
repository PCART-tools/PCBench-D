    def __iter__(self):
        sdata = self._get_sorted_data()

        if self.ngroups == 0:
            # we are inside a generator, rather than raise StopIteration
            # we merely return signal the end
            return

        starts, ends = lib.generate_slices(self.slabels, self.ngroups)

        for i, (start, end) in enumerate(zip(starts, ends)):
            # Since I'm now compressing the group ids, it's now not "possible"
            # to produce empty slices because such groups would not be observed
            # in the data
            # if start >= end:
            #     raise AssertionError('Start %s must be less than end %s'
            #                          % (str(start), str(end)))
            yield i, self._chop(sdata, slice(start, end))
