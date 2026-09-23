    def _downsample(self, how, **kwargs):
        """
        Downsample the cython defined function.

        Parameters
        ----------
        how : string / cython mapped function
        **kwargs : kw args passed to how function
        """
        orig_how = how
        how = com.get_cython_func(how) or how
        if orig_how != how:
            warn_alias_replacement(self, orig_how, how)
        ax = self.ax

        # Excludes `on` column when provided
        obj = self._obj_with_exclusions

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
        if self.axis == 0:
            result = obj.groupby(self.grouper).aggregate(how, **kwargs)
        else:
            # test_resample_axis1
            result = obj.T.groupby(self.grouper).aggregate(how, **kwargs).T

        return self._wrap_result(result)
