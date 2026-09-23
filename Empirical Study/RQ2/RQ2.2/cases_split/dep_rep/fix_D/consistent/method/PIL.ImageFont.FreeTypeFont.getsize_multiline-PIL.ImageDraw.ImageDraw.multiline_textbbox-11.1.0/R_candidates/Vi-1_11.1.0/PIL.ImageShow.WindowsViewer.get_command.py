    def get_command(self, file: str, **options: Any) -> str:
        return (
            f'start "Pillow" /WAIT "{file}" '
            "&& ping -n 4 127.0.0.1 >NUL "
            f'&& del /f "{file}"'
        )
