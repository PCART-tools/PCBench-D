    def tell(self) -> int:
        if not _webp.HAVE_WEBPANIM:
            return super().tell()

        return self.__logical_frame
