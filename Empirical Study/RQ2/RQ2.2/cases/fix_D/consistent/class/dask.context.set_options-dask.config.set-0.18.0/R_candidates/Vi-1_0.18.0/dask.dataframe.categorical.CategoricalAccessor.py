class CategoricalAccessor(Accessor):
    """
    Accessor object for categorical properties of the Series values.

    Examples
    --------
    >>> s.cat.categories  # doctest: +SKIP

    Notes
    -----
    Attributes that depend only on metadata are eager

    * categories
    * ordered

    Attributes depending on the entire dataset are lazy

    * codes
    * ...

    So `df.a.cat.categories` <=> `df.a._meta.cat.categories`
    So `df.a.cat.codes` <=> `df.a.map_partitions(lambda x: x.cat.codes)`
    """
    _accessor = pd.Series.cat
    _accessor_name = 'cat'

    def _validate(self, series):
        if not is_categorical_dtype(series.dtype):
            raise AttributeError("Can only use .cat accessor with a "
                                 "'category' dtype")

    @property
    def known(self):
        """Whether the categories are fully known"""
        return has_known_categories(self._series)

    def as_known(self, **kwargs):
        """Ensure the categories in this series are known.

        If the categories are known, this is a no-op. If unknown, the
        categories are computed, and a new series with known categories is
        returned.

        Parameters
        ----------
        kwargs
            Keywords to pass on to the call to `compute`.
        """
        if self.known:
            return self
        categories = self._property_map('categories').unique().compute(**kwargs)
        return self.set_categories(categories.values)

    def as_unknown(self):
        """Ensure the categories in this series are unknown"""
        if not self.known:
            return self._series
        out = self._series.copy()
        out._meta = clear_known_categories(out._meta)
        return out

    @property
    def ordered(self):
        return self._delegate_property(self._series._meta, 'cat', 'ordered')

    @property
    def categories(self):
        """The categories of this categorical.

        If categories are unknown, an error is raised"""
        if not self.known:
            msg = ("`df.column.cat.categories` with unknown categories is not "
                   "supported.  Please use `column.cat.as_known()` or "
                   "`df.categorize()` beforehand to ensure known categories")
            raise NotImplementedError(msg)
        return self._delegate_property(self._series._meta, 'cat', 'categories')

    @property
    def codes(self):
        """The codes of this categorical.

        If categories are unknown, an error is raised"""
        if not self.known:
            msg = ("`df.column.cat.codes` with unknown categories is not "
                   "supported.  Please use `column.cat.as_known()` or "
                   "`df.categorize()` beforehand to ensure known categories")
            raise NotImplementedError(msg)
        return self._property_map('codes')

    def remove_unused_categories(self):
        """
        Removes categories which are not used

        Notes
        -----
        This method requires a full scan of the data to compute the
        unique values, which can be expensive.
        """
        # get the set of used categories
        present = self._series.dropna().unique()
        present = pd.Index(present.compute())

        if isinstance(self._series._meta, pd.CategoricalIndex):
            meta_cat = self._series._meta
        else:
            meta_cat = self._series._meta.cat

        # Reorder to keep cat:code relationship, filtering unused (-1)
        ordered, mask = present.reindex(meta_cat.categories)
        new_categories = ordered[mask != -1]
        meta = meta_cat.set_categories(new_categories, ordered=meta_cat.ordered)
        return self._series.map_partitions(self._delegate_method, 'cat',
                                           'set_categories', (),
                                           {'new_categories': new_categories},
                                           meta=meta,
                                           token='cat-set_categories')
