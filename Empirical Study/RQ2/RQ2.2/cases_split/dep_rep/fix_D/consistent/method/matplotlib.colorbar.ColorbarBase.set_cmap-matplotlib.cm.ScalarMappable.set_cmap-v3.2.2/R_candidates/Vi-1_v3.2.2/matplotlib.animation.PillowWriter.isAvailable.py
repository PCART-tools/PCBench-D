    @classmethod
    def isAvailable(cls):
        try:
            import PIL
        except ImportError:
            return False
        return True
