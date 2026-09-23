    def __contains__(self, item: Any) -> bool:
        if item is None:
            return self.has_nulls()
        return self.implode().list.contains(item).item()
