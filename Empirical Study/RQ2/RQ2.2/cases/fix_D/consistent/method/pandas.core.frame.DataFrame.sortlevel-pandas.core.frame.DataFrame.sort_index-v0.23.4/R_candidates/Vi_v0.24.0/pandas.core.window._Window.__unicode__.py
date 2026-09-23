    def __unicode__(self):
        """
        Provide a nice str repr of our rolling object.
        """

        attrs = ["{k}={v}".format(k=k, v=getattr(self, k))
                 for k in self._attributes
                 if getattr(self, k, None) is not None]
        return "{klass} [{attrs}]".format(klass=self._window_type,
                                          attrs=','.join(attrs))
