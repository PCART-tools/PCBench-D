    @classmethod
    @Appender(_interval_shared_docs['from_tuples'] % _shared_docs_kwargs)
    def from_tuples(cls, data, closed='right', copy=False, dtype=None):
        if len(data):
            left, right = [], []
        else:
            # ensure that empty data keeps input dtype
            left = right = data

        for d in data:
            if isna(d):
                lhs = rhs = np.nan
            else:
                name = cls.__name__
                try:
                    # need list of length 2 tuples, e.g. [(0, 1), (1, 2), ...]
                    lhs, rhs = d
                except ValueError:
                    msg = ('{name}.from_tuples requires tuples of '
                           'length 2, got {tpl}').format(name=name, tpl=d)
                    raise ValueError(msg)
                except TypeError:
                    msg = ('{name}.from_tuples received an invalid '
                           'item, {tpl}').format(name=name, tpl=d)
                    raise TypeError(msg)
            left.append(lhs)
            right.append(rhs)

        return cls.from_arrays(left, right, closed, copy=False,
                               dtype=dtype)
