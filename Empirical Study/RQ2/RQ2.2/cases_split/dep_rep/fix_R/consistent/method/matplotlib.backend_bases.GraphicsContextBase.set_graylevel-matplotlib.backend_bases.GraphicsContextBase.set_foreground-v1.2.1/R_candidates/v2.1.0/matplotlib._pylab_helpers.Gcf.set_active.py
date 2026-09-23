    @classmethod
    def set_active(cls, manager):
        """
        Make the figure corresponding to *manager* the active one.
        """
        oldQue = cls._activeQue[:]
        cls._activeQue = []
        for m in oldQue:
            if m != manager:
                cls._activeQue.append(m)
        cls._activeQue.append(manager)
        cls.figs[manager.num] = manager
