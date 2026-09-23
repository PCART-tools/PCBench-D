@tensordot_lookup.register_lazy('sparse')
@concatenate_lookup.register_lazy('sparse')
def register_sparse():
    import sparse
    concatenate_lookup.register(sparse.COO, sparse.concatenate)
    tensordot_lookup.register(sparse.COO, sparse.tensordot)
