    @staticmethod
    def format_shortcut(key_sequence):
        """
        Convert a shortcut string from the notation used in rc config to the
        standard notation for displaying shortcuts, e.g. 'ctrl+a' -> 'Ctrl+A'.
        """
        return (key_sequence if len(key_sequence) == 1 else
                re.sub(r"\+[A-Z]", r"+Shift\g<0>", key_sequence).title())
