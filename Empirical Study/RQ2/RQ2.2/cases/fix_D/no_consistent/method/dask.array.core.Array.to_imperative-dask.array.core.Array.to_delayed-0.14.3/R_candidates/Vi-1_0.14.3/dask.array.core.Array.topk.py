    @wraps(topk)
    def topk(self, k):
        return topk(k, self)
