def can_hold_element(arr: ArrayLike, element: Any) -> bool:
    """
    Can we do an inplace setitem with this element in an array with this dtype?

    Parameters
    ----------
    arr : np.ndarray or ExtensionArray
    element : Any

    Returns
    -------
    bool
    """
    dtype = arr.dtype
    if not isinstance(dtype, np.dtype) or dtype.kind in ["m", "M"]:
        if isinstance(dtype, (PeriodDtype, IntervalDtype, DatetimeTZDtype, np.dtype)):
            # np.dtype here catches datetime64ns and timedelta64ns; we assume
            #  in this case that we have DatetimeArray/TimedeltaArray
            arr = cast(
                "PeriodArray | DatetimeArray | TimedeltaArray | IntervalArray", arr
            )
            try:
                arr._validate_setitem_value(element)
                return True
            except (ValueError, TypeError):
                return False

        # This is technically incorrect, but maintains the behavior of
        # ExtensionBlock._can_hold_element
        return True

    tipo = maybe_infer_dtype_type(element)

    if dtype.kind in ["i", "u"]:
        if tipo is not None:
            if tipo.kind not in ["i", "u"]:
                if is_float(element) and element.is_integer():
                    return True
                # Anything other than integer we cannot hold
                return False
            elif dtype.itemsize < tipo.itemsize:
                return False
            elif not isinstance(tipo, np.dtype):
                # i.e. nullable IntegerDtype; we can put this into an ndarray
                #  losslessly iff it has no NAs
                return not element._mask.any()
            return True

        # We have not inferred an integer from the dtype
        # check if we have a builtin int or a float equal to an int
        return is_integer(element) or (is_float(element) and element.is_integer())

    elif dtype.kind == "f":
        if tipo is not None:
            # TODO: itemsize check?
            if tipo.kind not in ["f", "i", "u"]:
                # Anything other than float/integer we cannot hold
                return False
            elif not isinstance(tipo, np.dtype):
                # i.e. nullable IntegerDtype or FloatingDtype;
                #  we can put this into an ndarray losslessly iff it has no NAs
                return not element._mask.any()
            return True

        return lib.is_integer(element) or lib.is_float(element)

    elif dtype.kind == "c":
        if tipo is not None:
            return tipo.kind in ["c", "f", "i", "u"]
        return (
            lib.is_integer(element) or lib.is_complex(element) or lib.is_float(element)
        )

    elif dtype.kind == "b":
        if tipo is not None:
            return tipo.kind == "b"
        return lib.is_bool(element)

    # error: Non-overlapping equality check (left operand type: "dtype[Any]", right
    # operand type: "Type[object]")
    elif dtype == object:  # type: ignore[comparison-overlap]
        return True

    elif dtype.kind == "S":
        # TODO: test tests.frame.methods.test_replace tests get here,
        #  need more targeted tests.  xref phofl has a PR about this
        if tipo is not None:
            return tipo.kind == "S" and tipo.itemsize <= dtype.itemsize
        return isinstance(element, bytes) and len(element) <= dtype.itemsize

    raise NotImplementedError(dtype)
