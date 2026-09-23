    @staticmethod
    def _text(value):
        """Converts text values into utf-8 or ascii strings.
        """
        if isinstance(value, bytes):
            value = value.decode(encoding='utf-8')
        elif not isinstance(value, str):
            value = str(value)
        return value
