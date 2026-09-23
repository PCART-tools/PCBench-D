    def __init__(self, index, grouper=None, obj=None, name=None, level=None,
                 sort=True, in_axis=False):

        self.name = name
        self.level = level
        self.grouper = _convert_grouper(index, grouper)
        self.index = index
        self.sort = sort
        self.obj = obj
        self.in_axis = in_axis

        # right place for this?
        if isinstance(grouper, (Series, Index)) and name is None:
            self.name = grouper.name

        if isinstance(grouper, MultiIndex):
            self.grouper = grouper.values

        # pre-computed
        self._should_compress = True

        # we have a single grouper which may be a myriad of things, some of which are
        # dependent on the passing in level
        #

        if level is not None:
            if not isinstance(level, int):
                if level not in index.names:
                    raise AssertionError('Level %s not in index' % str(level))
                level = index.names.index(level)

            inds = index.labels[level]
            level_index = index.levels[level]

            if self.name is None:
                self.name = index.names[level]

            # XXX complete hack

            if grouper is not None:
                level_values = index.levels[level].take(inds)
                self.grouper = level_values.map(self.grouper)
            else:
                # all levels may not be observed
                labels, uniques = algos.factorize(inds, sort=True)

                if len(uniques) > 0 and uniques[0] == -1:
                    # handle NAs
                    mask = inds != -1
                    ok_labels, uniques = algos.factorize(inds[mask], sort=True)

                    labels = np.empty(len(inds), dtype=inds.dtype)
                    labels[mask] = ok_labels
                    labels[~mask] = -1

                if len(uniques) < len(level_index):
                    level_index = level_index.take(uniques)

                self._labels = labels
                self._group_index = level_index
                self.grouper = level_index.take(labels)
        else:
            if isinstance(self.grouper, (list, tuple)):
                self.grouper = com._asarray_tuplesafe(self.grouper)

            # a passed Categorical
            elif is_categorical_dtype(self.grouper):

                # must have an ordered categorical
                if self.sort:
                    if not self.grouper.ordered:

                        # technically we cannot group on an unordered Categorical
                        # but this a user convenience to do so; the ordering
                        # is preserved and if its a reduction is doesnt't make any difference
                        pass

                # fix bug #GH8868 sort=False being ignored in categorical groupby
                else:
                    self.grouper = self.grouper.reorder_categories(self.grouper.unique())

                # we make a CategoricalIndex out of the cat grouper
                # preserving the categories / ordered attributes
                self._labels = self.grouper.codes

                c = self.grouper.categories
                self._group_index = CategoricalIndex(Categorical.from_codes(np.arange(len(c)),
                                                     categories=c,
                                                     ordered=self.grouper.ordered))
                if self.name is None:
                    self.name = self.grouper.name

            # a passed Grouper like
            elif isinstance(self.grouper, Grouper):

                # get the new grouper
                grouper = self.grouper._get_binner_for_grouping(self.obj)
                self.obj = self.grouper.obj
                self.grouper = grouper
                if self.name is None:
                    self.name = grouper.name

            # we are done
            if isinstance(self.grouper, Grouping):
                self.grouper = self.grouper.grouper

            # no level passed
            elif not isinstance(self.grouper, (Series, Index, Categorical, np.ndarray)):
                if getattr(self.grouper, 'ndim', 1) != 1:
                    t = self.name or str(type(self.grouper))
                    raise ValueError("Grouper for '%s' not 1-dimensional" % t)
                self.grouper = self.index.map(self.grouper)
                if not (hasattr(self.grouper, "__len__") and
                        len(self.grouper) == len(self.index)):
                    errmsg = ('Grouper result violates len(labels) == '
                              'len(data)\nresult: %s' %
                              com.pprint_thing(self.grouper))
                    self.grouper = None  # Try for sanity
                    raise AssertionError(errmsg)

        # if we have a date/time-like grouper, make sure that we have Timestamps like
        if getattr(self.grouper,'dtype',None) is not None:
            if is_datetime64_dtype(self.grouper):
                from pandas import to_datetime
                self.grouper = to_datetime(self.grouper)
            elif is_timedelta64_dtype(self.grouper):
                from pandas import to_timedelta
                self.grouper = to_timedelta(self.grouper)
