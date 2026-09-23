    @classmethod
    def destroy(cls, num):
        """
        Try to remove all traces of figure *num*.

        In the interactive backends, this is bound to the
        window "destroy" and "delete" events.
        """
        if not cls.has_fignum(num):
            return
        manager = cls.figs[num]
        manager.canvas.mpl_disconnect(manager._cidgcf)

        # There must be a good reason for the following careful
        # rebuilding of the activeQue; what is it?
        oldQue = cls._activeQue[:]
        cls._activeQue = []
        for f in oldQue:
            if f != manager:
                cls._activeQue.append(f)

        del cls.figs[num]
        manager.destroy()
        gc.collect(1)
