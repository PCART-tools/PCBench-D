    def _ignore_comments(self, block: bytes) -> bytes:
        if self._comment_spans:
            # Finish current comment
            while block:
                comment_end = self._find_comment_end(block)
                if comment_end != -1:
                    # Comment ends in this block
                    # Delete tail of comment
                    block = block[comment_end + 1 :]
                    break
                else:
                    # Comment spans whole block
                    # So read the next block, looking for the end
                    block = self._read_block()

        # Search for any further comments
        self._comment_spans = False
        while True:
            comment_start = block.find(b"#")
            if comment_start == -1:
                # No comment found
                break
            comment_end = self._find_comment_end(block, comment_start)
            if comment_end != -1:
                # Comment ends in this block
                # Delete comment
                block = block[:comment_start] + block[comment_end + 1 :]
            else:
                # Comment continues to next block(s)
                block = block[:comment_start]
                self._comment_spans = True
                break
        return block
