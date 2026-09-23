    def _contains(self, other):
        """sympy.sets uses the _contains method, so include it for compatibility."""

        if isinstance(other, Set) and other.is_FiniteSet:
            return all(self.__contains__(i) for i in other)

        return self.__contains__(other)
