    def __bool__(self) -> bool:
        for _ in self.jar:
            return True
        return False
