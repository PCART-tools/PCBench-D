    def __invert__(self):
        if not self.size:
            # inv fails with 0 len
            return self

        new_data = self._data.apply(operator.invert)
        result = self._constructor(new_data).__finalize__(self)
        return result
