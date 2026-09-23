    def __init__(self, axis, nonpos='mask'):
        """
        *nonpos*: {'mask', 'clip'}
          values beyond ]0, 1[ can be masked as invalid, or clipped to a number
          very close to 0 or 1
        """
        if nonpos not in ['mask', 'clip']:
            raise ValueError("nonposx, nonposy kwarg must be 'mask' or 'clip'")

        self._transform = LogitTransform(nonpos)
