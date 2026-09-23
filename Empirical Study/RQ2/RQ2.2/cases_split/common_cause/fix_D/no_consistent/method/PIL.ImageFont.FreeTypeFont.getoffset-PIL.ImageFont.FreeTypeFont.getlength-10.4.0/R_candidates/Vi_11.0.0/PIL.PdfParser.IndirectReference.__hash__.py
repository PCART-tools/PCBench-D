    def __hash__(self) -> int:
        return hash((self.object_id, self.generation))
