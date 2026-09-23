    def __eq__(self, other):
        if isinstance(other, BaseModel):
            return self.dict() == other.dict()
        else:
            return self.dict() == other
