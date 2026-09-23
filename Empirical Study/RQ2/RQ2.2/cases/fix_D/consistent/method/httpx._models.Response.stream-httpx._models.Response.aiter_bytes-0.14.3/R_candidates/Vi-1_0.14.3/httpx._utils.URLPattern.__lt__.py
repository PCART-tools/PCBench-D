    def __lt__(self, other: "URLPattern") -> bool:
        return self.priority < other.priority
