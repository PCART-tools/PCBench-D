    @classmethod
    def get_active(cls):
        """
        Return the manager of the active figure, or *None*.
        """
        if len(cls._activeQue) == 0:
            return None
        else:
            return cls._activeQue[-1]
