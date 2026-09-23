def OpAlmostEqual(op_a, op_b, ignore_fields=None):
    '''
    Two ops are identical except for each field in the `ignore_fields`.
    '''
    ignore_fields = ignore_fields or []
    if not isinstance(ignore_fields, list):
        ignore_fields = [ignore_fields]

    assert all(isinstance(f, text_type) for f in ignore_fields), (
        'Expect each field is text type, but got {}'.format(ignore_fields))

    def clean_op(op):
        op = copy.deepcopy(op)
        for field in ignore_fields:
            if op.HasField(field):
                op.ClearField(field)
        return op

    op_a = clean_op(op_a)
    op_b = clean_op(op_b)
    return op_a == op_b or str(op_a) == str(op_b)
