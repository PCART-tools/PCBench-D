    def __contains__(self, other):
        if super(Float64Index, self).__contains__(other):
            return True

        try:
            # if other is a sequence this throws a ValueError
            return np.isnan(other) and self._hasnans
        except ValueError:
            try:
                return len(other) <= 1 and _try_get_item(other) in self
            except TypeError:
                return False
        except:
            return False
