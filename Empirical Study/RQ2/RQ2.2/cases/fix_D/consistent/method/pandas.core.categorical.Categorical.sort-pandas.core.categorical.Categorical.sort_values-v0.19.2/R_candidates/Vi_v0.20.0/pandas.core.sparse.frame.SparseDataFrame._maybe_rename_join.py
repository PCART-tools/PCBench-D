    def _maybe_rename_join(self, other, lsuffix, rsuffix):
        to_rename = self.columns.intersection(other.columns)
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

            this = self.rename(columns=lrenamer)
            other = other.rename(columns=rrenamer)
        else:
            this = self

        return this, other
