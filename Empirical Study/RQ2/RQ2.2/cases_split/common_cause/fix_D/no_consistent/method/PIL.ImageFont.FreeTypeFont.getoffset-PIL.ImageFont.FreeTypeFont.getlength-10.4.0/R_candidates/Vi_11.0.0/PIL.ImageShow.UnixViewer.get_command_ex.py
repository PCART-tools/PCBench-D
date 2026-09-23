    @abc.abstractmethod
    def get_command_ex(self, file: str, **options: Any) -> tuple[str, str]:
        pass
