    def __init__(self):
        if not has_nose:
            raise ImportError("Need nose for this plugin.")
