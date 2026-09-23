def remap_input(op, blob_name_remapping):
    new_list = [blob_name_remapping.get(b, b) for b in op.input]
    del op.input[:]
    op.input.extend(new_list)
