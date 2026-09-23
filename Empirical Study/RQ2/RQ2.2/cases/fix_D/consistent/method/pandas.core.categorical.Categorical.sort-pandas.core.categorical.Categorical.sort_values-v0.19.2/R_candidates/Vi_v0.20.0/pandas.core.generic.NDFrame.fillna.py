    @Appender(_shared_docs['fillna'] % _shared_doc_kwargs)
    def fillna(self, value=None, method=None, axis=None, inplace=False,
               limit=None, downcast=None):
        inplace = validate_bool_kwarg(inplace, 'inplace')

        if isinstance(value, (list, tuple)):
            raise TypeError('"value" parameter must be a scalar or dict, but '
                            'you passed a "{0}"'.format(type(value).__name__))
        self._consolidate_inplace()

        # set the default here, so functions examining the signaure
        # can detect if something was set (e.g. in groupby) (GH9221)
        if axis is None:
            axis = 0
        axis = self._get_axis_number(axis)
        method = missing.clean_fill_method(method)
        from pandas import DataFrame
        if value is None:
            if method is None:
                raise ValueError('must specify a fill method or value')
            if self._is_mixed_type and axis == 1:
                if inplace:
                    raise NotImplementedError()
                result = self.T.fillna(method=method, limit=limit).T

                # need to downcast here because of all of the transposes
                result._data = result._data.downcast()

                return result

            # > 3d
            if self.ndim > 3:
                raise NotImplementedError('Cannot fillna with a method for > '
                                          '3dims')

            # 3d
            elif self.ndim == 3:

                # fill in 2d chunks
                result = dict([(col, s.fillna(method=method, value=value))
                               for col, s in self.iteritems()])
                new_obj = self._constructor.\
                    from_dict(result).__finalize__(self)
                new_data = new_obj._data

            else:
                # 2d or less
                method = missing.clean_fill_method(method)
                new_data = self._data.interpolate(method=method, axis=axis,
                                                  limit=limit, inplace=inplace,
                                                  coerce=True,
                                                  downcast=downcast)
        else:
            if method is not None:
                raise ValueError('cannot specify both a fill method and value')

            if len(self._get_axis(axis)) == 0:
                return self

            if self.ndim == 1:
                if isinstance(value, (dict, ABCSeries)):
                    from pandas import Series
                    value = Series(value)
                elif not is_list_like(value):
                    pass
                else:
                    raise ValueError("invalid fill value with a %s" %
                                     type(value))

                new_data = self._data.fillna(value=value, limit=limit,
                                             inplace=inplace,
                                             downcast=downcast)

            elif isinstance(value, (dict, ABCSeries)):
                if axis == 1:
                    raise NotImplementedError('Currently only can fill '
                                              'with dict/Series column '
                                              'by column')

                result = self if inplace else self.copy()
                for k, v in compat.iteritems(value):
                    if k not in result:
                        continue
                    obj = result[k]
                    obj.fillna(v, limit=limit, inplace=True, downcast=downcast)
                return result
            elif not is_list_like(value):
                new_data = self._data.fillna(value=value, limit=limit,
                                             inplace=inplace,
                                             downcast=downcast)
            elif isinstance(value, DataFrame) and self.ndim == 2:
                new_data = self.where(self.notnull(), value)
            else:
                raise ValueError("invalid fill value with a %s" % type(value))

        if inplace:
            self._update_inplace(new_data)
        else:
            return self._constructor(new_data).__finalize__(self)
