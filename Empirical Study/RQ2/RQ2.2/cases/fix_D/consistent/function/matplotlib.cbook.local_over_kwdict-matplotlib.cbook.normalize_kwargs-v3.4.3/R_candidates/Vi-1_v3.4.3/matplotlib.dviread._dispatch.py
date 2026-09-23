def _dispatch(table, min, max=None, state=None, args=('raw',)):
    """
    Decorator for dispatch by opcode. Sets the values in *table*
    from *min* to *max* to this method, adds a check that the Dvi state
    matches *state* if not None, reads arguments from the file according
    to *args*.

    *table*
        the dispatch table to be filled in

    *min*
        minimum opcode for calling this function

    *max*
        maximum opcode for calling this function, None if only *min* is allowed

    *state*
        state of the Dvi object in which these opcodes are allowed

    *args*
        sequence of argument specifications:

        ``'raw'``: opcode minus minimum
        ``'u1'``: read one unsigned byte
        ``'u4'``: read four bytes, treat as an unsigned number
        ``'s4'``: read four bytes, treat as a signed number
        ``'slen'``: read (opcode - minimum) bytes, treat as signed
        ``'slen1'``: read (opcode - minimum + 1) bytes, treat as signed
        ``'ulen1'``: read (opcode - minimum + 1) bytes, treat as unsigned
        ``'olen1'``: read (opcode - minimum + 1) bytes, treat as unsigned
                     if under four bytes, signed if four bytes
    """
    def decorate(method):
        get_args = [_arg_mapping[x] for x in args]

        @wraps(method)
        def wrapper(self, byte):
            if state is not None and self.state != state:
                raise ValueError("state precondition failed")
            return method(self, *[f(self, byte-min) for f in get_args])
        if max is None:
            table[min] = wrapper
        else:
            for i in range(min, max+1):
                assert table[i] is None
                table[i] = wrapper
        return wrapper
    return decorate
