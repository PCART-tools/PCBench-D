    def drop(self, labels, axis=0, level=None, inplace=False, **kwargs):
        """
        Return new object with labels in requested axis removed

        Parameters
        ----------
        labels : single label or list-like
        axis : int or axis name
        level : int or name, default None
            For MultiIndex
        inplace : bool, default False
            If True, do operation inplace and return None.

        Returns
        -------
        dropped : type of caller
        """
        axis = self._get_axis_number(axis)
        axis_name = self._get_axis_name(axis)
        axis, axis_ = self._get_axis(axis), axis

        if axis.is_unique:
            if level is not None:
                if not isinstance(axis, MultiIndex):
                    raise AssertionError('axis must be a MultiIndex')
                new_axis = axis.drop(labels, level=level)
            else:
                new_axis = axis.drop(labels)
            dropped = self.reindex(**{axis_name: new_axis})
            try:
                dropped.axes[axis_].set_names(axis.names, inplace=True)
            except AttributeError:
                pass
            result = dropped

        else:
            labels = com._index_labels_to_array(labels)
            if level is not None:
                if not isinstance(axis, MultiIndex):
                    raise AssertionError('axis must be a MultiIndex')
                indexer = -lib.ismember(axis.get_level_values(level),
                                        set(labels))
            else:
                indexer = -axis.isin(labels)

            slicer = [slice(None)] * self.ndim
            slicer[self._get_axis_number(axis_name)] = indexer

            result = self.ix[tuple(slicer)]

        if inplace:
            self._update_inplace(result)
        else:
            return result
