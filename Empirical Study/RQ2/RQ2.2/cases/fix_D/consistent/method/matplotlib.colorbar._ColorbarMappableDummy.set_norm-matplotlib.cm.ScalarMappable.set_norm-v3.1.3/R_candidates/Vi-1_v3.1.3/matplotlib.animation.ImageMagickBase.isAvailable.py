    @classmethod
    def isAvailable(cls):
        try:
            return super().isAvailable()
        except FileNotFoundError:  # May be raised by get_executable_info.
            return False
