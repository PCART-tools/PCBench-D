    def symmetric_difference(self, other, result_name: Hashable = None, sort=None):
        if not isinstance(other, RangeIndex) or sort is not None:
            return super().symmetric_difference(other, result_name, sort)

        left = self.difference(other)
        right = other.difference(self)
        result = left.union(right)

        if result_name is not None:
            result = result.rename(result_name)
        return result
