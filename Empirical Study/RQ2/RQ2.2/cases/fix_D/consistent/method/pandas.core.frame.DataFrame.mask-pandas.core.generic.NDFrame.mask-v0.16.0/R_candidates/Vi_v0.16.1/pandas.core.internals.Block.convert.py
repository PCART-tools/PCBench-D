    def convert(self, copy=True, **kwargs):
        """ attempt to coerce any object types to better types
            return a copy of the block (if copy = True)
            by definition we are not an ObjectBlock here!  """

        return [self.copy()] if copy else [self]
