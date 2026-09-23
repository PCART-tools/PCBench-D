    def _validate_partial_date_slice(self, reso: Resolution):
        assert isinstance(reso, Resolution), (type(reso), reso)
        grp = reso.freq_group
        freqn = self.dtype.freq_group

        if not grp < freqn:
            # TODO: we used to also check for
            #  reso in ["day", "hour", "minute", "second"]
            #  why is that check not needed?
            raise ValueError
