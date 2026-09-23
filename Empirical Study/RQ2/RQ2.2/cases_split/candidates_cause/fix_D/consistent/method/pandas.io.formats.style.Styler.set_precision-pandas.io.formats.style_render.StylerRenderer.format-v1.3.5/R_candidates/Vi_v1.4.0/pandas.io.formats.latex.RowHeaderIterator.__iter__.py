    def __iter__(self) -> Iterator[str]:
        for row_num in range(len(self.strrows)):
            if row_num < self._header_row_num:
                yield self.get_strrow(row_num)
