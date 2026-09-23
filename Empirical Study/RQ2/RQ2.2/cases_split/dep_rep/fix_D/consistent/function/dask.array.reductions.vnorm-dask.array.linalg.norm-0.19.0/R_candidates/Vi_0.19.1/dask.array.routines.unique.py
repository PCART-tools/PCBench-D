@wraps(np.unique)
def unique(ar, return_index=False, return_inverse=False, return_counts=False):
    ar = ar.ravel()

    # Run unique on each chunk and collect results in a Dask Array of
    # unknown size.

    args = [ar, "i"]
    out_dtype = [("values", ar.dtype)]
    if return_index:
        args.extend([
            arange(ar.shape[0], dtype=np.intp, chunks=ar.chunks[0]),
            "i"
        ])
        out_dtype.append(("indices", np.intp))
    else:
        args.extend([None, None])
    if return_counts:
        args.extend([
            ones((ar.shape[0],), dtype=np.intp, chunks=ar.chunks[0]),
            "i"
        ])
        out_dtype.append(("counts", np.intp))
    else:
        args.extend([None, None])

    out = atop(
        _unique_internal, "i",
        *args,
        dtype=out_dtype,
        return_inverse=False
    )
    out._chunks = tuple((np.nan,) * len(c) for c in out.chunks)

    # Take the results from the unique chunks and do the following.
    #
    # 1. Collect all results as arguments.
    # 2. Concatenate each result into one big array.
    # 3. Pass all results as arguments to the internal unique again.
    #
    # TODO: This should be replaced with a tree reduction using this strategy.
    # xref: https://github.com/dask/dask/issues/2851

    out_parts = [out["values"]]
    if return_index:
        out_parts.append(out["indices"])
    else:
        out_parts.append(None)
    if return_counts:
        out_parts.append(out["counts"])
    else:
        out_parts.append(None)

    name = 'unique-aggregate-' + out.name
    dsk = {
        (name, 0): (
            (_unique_internal,) +
            tuple(
                (np.concatenate, o. __dask_keys__())
                if hasattr(o, "__dask_keys__") else o
                for o in out_parts
            ) +
            (return_inverse,)
        )
    }
    out_dtype = [("values", ar.dtype)]
    if return_index:
        out_dtype.append(("indices", np.intp))
    if return_inverse:
        out_dtype.append(("inverse", np.intp))
    if return_counts:
        out_dtype.append(("counts", np.intp))

    out = Array(
        sharedict.merge(*(
            [(name, dsk)] +
            [o.dask for o in out_parts if hasattr(o, "__dask_keys__")]
        )),
        name,
        ((np.nan,),),
        out_dtype
    )

    # Split out all results to return to the user.

    result = [out["values"]]
    if return_index:
        result.append(out["indices"])
    if return_inverse:
        # Using the returned unique values and arange of unknown length, find
        # each value matching a unique value and replace it with its
        # corresponding index or `0`. There should be only one entry for this
        # index in axis `1` (the one of unknown length). Reduce axis `1`
        # through summing to get an array with known dimensionality and the
        # mapping of the original values.
        mtches = (ar[:, None] == out["values"][None, :]).astype(np.intp)
        result.append((mtches * out["inverse"]).sum(axis=1))
    if return_counts:
        result.append(out["counts"])

    if len(result) == 1:
        result = result[0]
    else:
        result = tuple(result)

    return result
