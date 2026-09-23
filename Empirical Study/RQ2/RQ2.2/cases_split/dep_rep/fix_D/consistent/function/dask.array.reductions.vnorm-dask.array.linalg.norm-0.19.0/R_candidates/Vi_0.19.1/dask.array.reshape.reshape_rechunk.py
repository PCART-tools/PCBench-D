def reshape_rechunk(inshape, outshape, inchunks):
    assert all(isinstance(c, tuple) for c in inchunks)
    ii = len(inshape) - 1
    oi = len(outshape) - 1
    result_inchunks = [None for i in range(len(inshape))]
    result_outchunks = [None for i in range(len(outshape))]

    while ii >= 0 or oi >= 0:
        if inshape[ii] == outshape[oi]:
            result_inchunks[ii] = inchunks[ii]
            result_outchunks[oi] = inchunks[ii]
            ii -= 1
            oi -= 1
            continue
        din = inshape[ii]
        dout = outshape[oi]
        if din == 1:
            result_inchunks[ii] = (1,)
            ii -= 1
        elif dout == 1:
            result_outchunks[oi] = (1,)
            oi -= 1
        elif din < dout:  # (4, 4, 4) -> (64,)
            ileft = ii - 1
            while ileft >= 0 and reduce(mul, inshape[ileft:ii + 1]) < dout: # 4 < 64, 4*4 < 64, 4*4*4 == 64
                ileft -= 1
            if reduce(mul, inshape[ileft:ii + 1]) != dout:
                raise ValueError("Shapes not compatible")

            for i in range(ileft + 1, ii + 1):  # need single-shape dimensions
                result_inchunks[i] = (inshape[i],)  # chunks[i] = (4,)

            chunk_reduction = reduce(mul, map(len, inchunks[ileft + 1:ii + 1]))
            result_inchunks[ileft] = expand_tuple(inchunks[ileft], chunk_reduction)

            prod = reduce(mul, inshape[ileft + 1: ii + 1])  # 16
            result_outchunks[oi] = tuple(prod * c for c in result_inchunks[ileft]) # (1, 1, 1, 1) .* 16

            oi -= 1
            ii = ileft - 1
        elif din > dout:  # (64,) -> (4, 4, 4)
            oleft = oi - 1
            while oleft >= 0 and reduce(mul, outshape[oleft:oi + 1]) < din:
                oleft -= 1
            if reduce(mul, outshape[oleft:oi + 1]) != din:
                raise ValueError("Shapes not compatible")

            # TODO: don't coalesce shapes unnecessarily
            cs = reduce(mul, outshape[oleft + 1: oi + 1])

            result_inchunks[ii] = contract_tuple(inchunks[ii], cs) # (16, 16, 16, 16)

            for i in range(oleft + 1, oi + 1):
                result_outchunks[i] = (outshape[i],)

            result_outchunks[oleft] = tuple(c // cs for c in result_inchunks[ii])

            oi = oleft - 1
            ii -= 1

    return tuple(result_inchunks), tuple(result_outchunks)
