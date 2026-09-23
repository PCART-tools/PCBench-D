    def _replace_single(self, to_replace, value, inplace=False, filter=None,
                        regex=False):
        # to_replace is regex compilable
        to_rep_re = com.is_re_compilable(to_replace)

        # regex is regex compilable
        regex_re = com.is_re_compilable(regex)

        # only one will survive
        if to_rep_re and regex_re:
            raise AssertionError('only one of to_replace and regex can be '
                                 'regex compilable')

        # if regex was passed as something that can be a regex (rather than a
        # boolean)
        if regex_re:
            to_replace = regex

        regex = regex_re or to_rep_re

        # try to get the pattern attribute (compiled re) or it's a string
        try:
            pattern = to_replace.pattern
        except AttributeError:
            pattern = to_replace

        # if the pattern is not empty and to_replace is either a string or a
        # regex
        if regex and pattern:
            rx = re.compile(to_replace)
        else:
            # if the thing to replace is not a string or compiled regex call
            # the superclass method -> to_replace is some kind of object
            result = super(ObjectBlock, self).replace(to_replace, value,
                                                      inplace=inplace,
                                                      filter=filter,
                                                      regex=regex)
            if not isinstance(result, list):
                result = [result]
            return result

        new_values = self.values if inplace else self.values.copy()

        # deal with replacing values with objects (strings) that match but
        # whose replacement is not a string (numeric, nan, object)
        if isnull(value) or not isinstance(value, compat.string_types):
            def re_replacer(s):
                try:
                    return value if rx.search(s) is not None else s
                except TypeError:
                    return s
        else:
            # value is guaranteed to be a string here, s can be either a string
            # or null if it's null it gets returned
            def re_replacer(s):
                try:
                    return rx.sub(value, s)
                except TypeError:
                    return s

        f = np.vectorize(re_replacer, otypes=[self.dtype])

        try:
            filt = lmap(self.items.get_loc, filter)
        except TypeError:
            filt = slice(None)

        new_values[filt] = f(new_values[filt])

        return [self if inplace else make_block(new_values, self.items,
                                                self.ref_items, fastpath=True)]
