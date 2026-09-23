    def _maybe_rename_join(self, other, lsuffix, rsuffix, copydata=True):
        to_rename = self.items.intersection(other.items)
        if len(to_rename) > 0:
            if not lsuffix and not rsuffix:
                raise ValueError('columns overlap but no suffix specified: %s'
                                 % to_rename)

            def lrenamer(x):
                if x in to_rename:
                    return '%s%s' % (x, lsuffix)
                return x

            def rrenamer(x):
                if x in to_rename:
                    return '%s%s' % (x, rsuffix)
                return x

            this = self.rename_items(lrenamer, copy=copydata)
            other = other.rename_items(rrenamer, copy=copydata)
        else:
            this = self

        return this, other
