    def _downsample(self, how, **kwargs):
        """
        Downsample the cython defined function.

        Parameters
        ----------
        how : string / cython mapped function
        **kwargs : kw args passed to how function
        """
        how = com.get_cython_func(how) or how
        ax = self.ax
        obj = self._selected_obj

        if not len(ax):
            # reset to the new freq
            obj = obj.copy()
            obj.index = obj.index._with_freq(self.freq)
            assert obj.index.freq == self.freq, (obj.index.freq, self.freq)
            return obj

        # do we have a regular frequency

        # error: Item "None" of "Optional[Any]" has no attribute "binlabels"
        if (
            (ax.freq is not None or ax.inferred_freq is not None)
            and len(self.grouper.binlabels) > len(ax)
            and how is None
        ):

            # let's do an asfreq
            return self.asfreq()

        # we are downsampling
        # we want to call the actual grouper method here
        result = obj.groupby(self.grouper, axis=self.axis).aggregate(how, **kwargs)

        result = self._apply_loffset(result)
        return self._wrap_result(result)
