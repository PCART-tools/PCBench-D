    def __invert__(self):
        try:
            arr = operator.inv(_values_from_object(self))
            return self.__array_wrap__(arr)
        except:

            # inv fails with 0 len
            if not np.prod(self.shape):
                return self

            raise
