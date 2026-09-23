def _destruct_iterable_mapping_values(data):
    for i, elem in enumerate(data):
        if len(elem) != 2:
            raise ValueError(
                'dictionary update sequence element #{} has '
                'length {}; 2 is required.'.format(i, len(elem))
            )
        if not isinstance(elem[0], str):
            raise ValueError('Element key %r invalid, only strings are allowed' % elem[0])
        yield tuple(elem)
