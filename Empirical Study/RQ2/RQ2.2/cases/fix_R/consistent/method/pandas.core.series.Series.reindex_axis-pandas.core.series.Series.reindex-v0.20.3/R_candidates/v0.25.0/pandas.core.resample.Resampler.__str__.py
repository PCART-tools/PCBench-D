    def __str__(self):
        """
        Provide a nice str repr of our rolling object.
        """
        attrs = (
            "{k}={v}".format(k=k, v=getattr(self.groupby, k))
            for k in self._attributes
            if getattr(self.groupby, k, None) is not None
        )
        return "{klass} [{attrs}]".format(
            klass=self.__class__.__name__, attrs=", ".join(attrs)
        )
