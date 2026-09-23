    def __repr__(self) -> str:
        if self.filter is None:
            return "Filter: Not Initialized"
        return pprint_thing(f"[Filter : [{self.filter[0]}] -> [{self.filter[1]}]")
