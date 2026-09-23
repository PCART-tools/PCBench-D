    @final
    def __invert__(self):
        if not self.size:
            # inv fails with 0 len
            return self

        new_data = self._mgr.apply(operator.invert)
        return self._constructor(new_data).__finalize__(self, method="__invert__")
