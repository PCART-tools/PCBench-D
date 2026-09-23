    @abstractmethod
    def freeze(self):
        """Freeze the match info.

        The method is called after route resolution.

        After the call .add_app() is forbidden.

        """
