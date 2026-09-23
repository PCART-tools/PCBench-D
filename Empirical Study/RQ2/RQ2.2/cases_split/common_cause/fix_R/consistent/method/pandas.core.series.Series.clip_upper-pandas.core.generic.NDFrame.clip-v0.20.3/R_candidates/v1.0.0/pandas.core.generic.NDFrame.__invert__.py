    def __invert__(self):
        if not self.size:
            # inv fails with 0 len
            return self

        arr = operator.inv(com.values_from_object(self))
        return self.__array_wrap__(arr)
