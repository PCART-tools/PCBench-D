def index_put_fallback(self, indices, values, accumulate):
    ir.IndexPutFallback(V.graph.current_node.target, self, indices, values, accumulate)
    return self
