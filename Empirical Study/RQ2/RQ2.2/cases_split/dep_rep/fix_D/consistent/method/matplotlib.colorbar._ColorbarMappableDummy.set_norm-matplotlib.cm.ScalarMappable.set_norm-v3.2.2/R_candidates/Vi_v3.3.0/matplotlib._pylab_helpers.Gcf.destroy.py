    @classmethod
    def destroy(cls, num):
        """
        Destroy manager *num* -- either a manager instance or a manager number.

        In the interactive backends, this is bound to the window "destroy" and
        "delete" events.

        It is recommended to pass a manager instance, to avoid confusion when
        two managers share the same number.
        """
        if all(hasattr(num, attr) for attr in ["num", "_cidgcf", "destroy"]):
            manager = num
            if cls.figs.get(manager.num) is manager:
                cls.figs.pop(manager.num)
            else:
                return
        else:
            try:
                manager = cls.figs.pop(num)
            except KeyError:
                return
        manager.canvas.mpl_disconnect(manager._cidgcf)
        manager.destroy()
        gc.collect(1)
