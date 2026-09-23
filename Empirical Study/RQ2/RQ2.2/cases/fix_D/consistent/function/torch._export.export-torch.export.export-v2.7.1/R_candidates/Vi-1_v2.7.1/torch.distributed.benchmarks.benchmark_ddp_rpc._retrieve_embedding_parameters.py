def _retrieve_embedding_parameters(emb_rref):
    return [RRef(p) for p in emb_rref.local_value().parameters()]
