    def __eq__(self, other):
        # other may not even have the attributes we are checking.
        return ((self._gridspec, self.num1, self.num2)
                == (getattr(other, "_gridspec", object()),
                    getattr(other, "num1", object()),
                    getattr(other, "num2", object())))
