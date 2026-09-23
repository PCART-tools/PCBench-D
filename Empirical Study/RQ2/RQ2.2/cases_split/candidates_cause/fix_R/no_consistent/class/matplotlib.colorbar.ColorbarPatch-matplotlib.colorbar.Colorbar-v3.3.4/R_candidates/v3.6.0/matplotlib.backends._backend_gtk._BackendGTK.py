class _BackendGTK(_Backend):
    @staticmethod
    def mainloop():
        global _application
        if _application is None:
            return

        try:
            _application.run()  # Quits when all added windows close.
        except KeyboardInterrupt:
            # Ensure all windows can process their close event from
            # _shutdown_application.
            context = GLib.MainContext.default()
            while context.pending():
                context.iteration(True)
            raise
        finally:
            # Running after quit is undefined, so create a new one next time.
            _application = None
