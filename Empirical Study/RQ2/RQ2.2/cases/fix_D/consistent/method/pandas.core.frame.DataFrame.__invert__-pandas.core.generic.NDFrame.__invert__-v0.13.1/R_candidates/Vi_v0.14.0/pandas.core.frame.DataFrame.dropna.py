    def dropna(self, axis=0, how='any', thresh=None, subset=None,
               inplace=False):
        """
        Return object with labels on given axis omitted where alternately any
        or all of the data are missing

        Parameters
        ----------
        axis : {0, 1}, or tuple/list thereof
            Pass tuple or list to drop on multiple axes
        how : {'any', 'all'}
            * any : if any NA values are present, drop that label
            * all : if all values are NA, drop that label
        thresh : int, default None
            int value : require that many non-NA values
        subset : array-like
            Labels along other axis to consider, e.g. if you are dropping rows
            these would be a list of columns to include
        inplace : boolean, defalt False
            If True, do operation inplace and return None.

        Returns
        -------
        dropped : DataFrame
        """
        if isinstance(axis, (tuple, list)):
            result = self
            for ax in axis:
                result = result.dropna(how=how, thresh=thresh,
                                       subset=subset, axis=ax)
        else:
            axis = self._get_axis_number(axis)
            agg_axis = 1 - axis

            agg_obj = self
            if subset is not None:
                ax = self._get_axis(agg_axis)
                agg_obj = self.take(ax.get_indexer_for(subset),axis=agg_axis)

            count = agg_obj.count(axis=agg_axis)

            if thresh is not None:
                mask = count >= thresh
            elif how == 'any':
                mask = count == len(agg_obj._get_axis(agg_axis))
            elif how == 'all':
                mask = count > 0
            else:
                if how is not None:
                    raise ValueError('invalid how option: %s' % how)
                else:
                    raise TypeError('must specify how or thresh')

            result = self.take(mask.nonzero()[0], axis=axis, convert=False)

        if inplace:
            self._update_inplace(result)
        else:
            return result
