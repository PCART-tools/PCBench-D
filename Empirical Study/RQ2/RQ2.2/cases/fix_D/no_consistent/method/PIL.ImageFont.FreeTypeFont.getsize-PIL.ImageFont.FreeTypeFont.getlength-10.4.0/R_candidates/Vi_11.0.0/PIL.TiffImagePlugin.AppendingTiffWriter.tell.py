    def tell(self) -> int:
        return self.f.tell() - self.offsetOfNewPage
