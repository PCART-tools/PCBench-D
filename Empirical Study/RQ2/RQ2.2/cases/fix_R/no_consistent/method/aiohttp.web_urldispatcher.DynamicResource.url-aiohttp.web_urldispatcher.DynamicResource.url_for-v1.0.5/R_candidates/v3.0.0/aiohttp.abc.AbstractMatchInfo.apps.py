    @property  # pragma: no branch
    @abstractmethod
    def apps(self):
        """Stack of nested applications.

        Top level application is left-most element.

        """
