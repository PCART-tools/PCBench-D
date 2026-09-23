    def __contains__(self, other):
        if super().__contains__(other):
            return True

        try:
            # if other is a sequence this throws a ValueError
            return np.isnan(other) and self.hasnans
        except ValueError:
            try:
                return len(other) <= 1 and other.item() in self
            except AttributeError:
                return len(other) <= 1 and other in self
            except TypeError:
                pass
        except TypeError:
            pass

        return False
