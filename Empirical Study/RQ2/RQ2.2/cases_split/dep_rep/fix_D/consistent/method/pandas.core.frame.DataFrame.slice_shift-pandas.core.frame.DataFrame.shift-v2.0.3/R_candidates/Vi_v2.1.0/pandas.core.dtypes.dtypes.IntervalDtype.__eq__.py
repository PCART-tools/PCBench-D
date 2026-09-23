    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return other.lower() in (self.name.lower(), str(self).lower())
        elif not isinstance(other, IntervalDtype):
            return False
        elif self.subtype is None or other.subtype is None:
            # None should match any subtype
            return True
        elif self.closed != other.closed:
            return False
        else:
            return self.subtype == other.subtype
