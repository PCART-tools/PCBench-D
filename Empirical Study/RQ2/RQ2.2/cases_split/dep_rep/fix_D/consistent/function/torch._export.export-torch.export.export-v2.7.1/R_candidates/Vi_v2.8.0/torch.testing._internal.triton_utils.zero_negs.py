    @triton.jit
    def zero_negs(x):
        return tl.where(x >= 0, x, 0)
