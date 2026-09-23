    def get_command(self, file: str, **options: Any) -> str:
        """
        Returns the command used to display the file.
        Not implemented in the base class.
        """
        msg = "unavailable in base viewer"
        raise NotImplementedError(msg)
