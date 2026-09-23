    def push(self, cid: bytes, pos: int, length: int) -> None:
        assert self.queue is not None
        self.queue.append((cid, pos, length))
