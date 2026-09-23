    def pchanged(self):
        """
        Fire an event when property changed, calling all of the
        registered callbacks.
        """
        for oid, func in list(six.iteritems(self._propobservers)):
            func(self)
