    @classmethod
    def start_main_loop(cls):
        """
        Start the main event loop.

        This method is called by `.FigureManagerBase.pyplot_show`, which is the
        implementation of `.pyplot.show`.  To customize the behavior of
        `.pyplot.show`, interactive backends should usually override
        `~.FigureManagerBase.start_main_loop`; if more customized logic is
        necessary, `~.FigureManagerBase.pyplot_show` can also be overridden.
        """
