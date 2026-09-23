    def get_app(self):
        """Obsolete method used to constructing web application.

        Use .get_application() coroutine instead

        """
        raise RuntimeError("Did you forget to define get_application()?")
