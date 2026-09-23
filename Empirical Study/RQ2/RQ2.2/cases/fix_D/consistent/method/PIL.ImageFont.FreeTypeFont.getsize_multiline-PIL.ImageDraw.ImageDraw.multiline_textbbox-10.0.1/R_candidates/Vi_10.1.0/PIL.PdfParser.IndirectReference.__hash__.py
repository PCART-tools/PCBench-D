    def __hash__(self):
        return hash((self.object_id, self.generation))
