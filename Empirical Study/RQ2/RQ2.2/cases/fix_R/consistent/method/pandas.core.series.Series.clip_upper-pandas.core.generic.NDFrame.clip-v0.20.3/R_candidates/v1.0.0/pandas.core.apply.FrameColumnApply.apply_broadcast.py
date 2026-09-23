    def apply_broadcast(self, target: "DataFrame") -> "DataFrame":
        result = super().apply_broadcast(target.T)
        return result.T
