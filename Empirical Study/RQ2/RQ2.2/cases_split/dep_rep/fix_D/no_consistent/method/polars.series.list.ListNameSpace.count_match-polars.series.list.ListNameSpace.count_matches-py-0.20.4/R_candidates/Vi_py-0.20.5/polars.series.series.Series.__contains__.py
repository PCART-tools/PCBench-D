    def __contains__(self, item: Any) -> bool:
        if item is None:
            return self.null_count() > 0
        return self.implode().list.contains(item).item()
