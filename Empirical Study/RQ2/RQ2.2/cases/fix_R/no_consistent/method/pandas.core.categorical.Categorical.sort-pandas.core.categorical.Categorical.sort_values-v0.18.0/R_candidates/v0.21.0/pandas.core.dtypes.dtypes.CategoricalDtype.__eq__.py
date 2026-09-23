    def __eq__(self, other):
        if isinstance(other, compat.string_types):
            return other == self.name

        if not (hasattr(other, 'ordered') and hasattr(other, 'categories')):
            return False
        elif self.categories is None or other.categories is None:
            # We're forced into a suboptimal corner thanks to math and
            # backwards compatibility. We require that `CDT(...) == 'category'`
            # for all CDTs **including** `CDT(None, ...)`. Therefore, *all*
            # CDT(., .) = CDT(None, False) and *all*
            # CDT(., .) = CDT(None, True).
            return True
        elif self.ordered:
            return other.ordered and self.categories.equals(other.categories)
        elif other.ordered:
            return False
        else:
            # both unordered; this could probably be optimized / cached
            return hash(self) == hash(other)
