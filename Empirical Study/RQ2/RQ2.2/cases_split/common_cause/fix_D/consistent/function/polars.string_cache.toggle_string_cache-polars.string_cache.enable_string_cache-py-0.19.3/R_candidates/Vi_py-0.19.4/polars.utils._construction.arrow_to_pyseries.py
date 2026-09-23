def arrow_to_pyseries(name: str, values: pa.Array, *, rechunk: bool = True) -> PySeries:
    """Construct a PySeries from an Arrow array."""
    array = coerce_arrow(values)

    # special handling of empty categorical arrays
    if (
        len(array) == 0
        and isinstance(array.type, pa.DictionaryType)
        and array.type.value_type
        in (
            pa.utf8(),
            pa.large_utf8(),
        )
    ):
        pys = pl.Series(name, [], dtype=Categorical)._s

    elif not hasattr(array, "num_chunks"):
        pys = PySeries.from_arrow(name, array)
    else:
        if array.num_chunks > 1:
            # somehow going through ffi with a structarray
            # returns the first chunk everytime
            if isinstance(array.type, pa.StructType):
                pys = PySeries.from_arrow(name, array.combine_chunks())
            else:
                it = array.iterchunks()
                pys = PySeries.from_arrow(name, next(it))
                for a in it:
                    pys.append(PySeries.from_arrow(name, a))
        elif array.num_chunks == 0:
            pys = PySeries.from_arrow(name, pa.array([], array.type))
        else:
            pys = PySeries.from_arrow(name, array.chunks[0])

        if rechunk:
            pys.rechunk(in_place=True)

    return pys
