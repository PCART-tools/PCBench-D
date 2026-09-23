def clone_and_bind_net(net, name, prefix, blob_remap=None, inputs=None,
                       keep_schema=True):
    """
    Clone the given Net, binding its input schema to the given `inputs` record.
    Blob names defined by the net are prepended with the given `prefix`.

    Args:
        net:        the net to clone
        name:       the name of the new net
        prefix:     the prefix to append to local blobs
        blob_remap: (optional) dict with additional blob name remapping.
        inputs:     (optional) input record that will provide actual input
                    values for the cloned net. Must be compatible with the
                    net's input schema or be a strict superset of it
        keep_schema: by default (True), the original schema will be kept and
                     remapped accordingly. otherwise, the schema will be set as
                     inputs or left empty if inputs is not given.
    Returns:
        Tuple (cloned_net, blob_remap)
        clone_net:  the cloned Net
        blob_remap: a map from original blob names into remapped blob names
    """
    from caffe2.python import schema
    assert isinstance(net, Net)
    if blob_remap is None:
        blob_remap = {}
    if inputs is not None:
        assert isinstance(inputs, schema.Field)
        original = net.input_record()
        assert original is not None
        # TODO(azzolini): improve schema type checking
        diff = set(original.field_names()) - set(inputs.field_names())
        assert len(diff) == 0, (
            "Schemas don't match, extra fields {diff} found in the net {name}. "
            "original: {original}; inputs: {inputs}"
            .format(
                diff=diff, name=net.Name(), original=original.field_names(),
                inputs=inputs.field_names()
            )
        )
        original_mapping = dict(zip(original.field_names(),
                                    original.field_blobs()))
        for fn, fb in zip(inputs.field_names(), inputs.field_blobs()):
            if fn in original_mapping:
                blob_remap[str(original_mapping[fn])] = str(fb)
    proto = net.Proto()
    ssa, blob_versions = get_ssa(proto)
    undef_blobs = get_undefined_blobs(ssa)

    for blob in viewkeys(blob_versions):
        if blob in blob_remap:
            continue
        elif blob in undef_blobs:
            blob_remap[blob] = blob
        else:
            blob_remap[blob] = prefix + blob
    cloned_net = net.Clone(name, blob_remap, keep_schema=keep_schema)
    if not keep_schema and inputs:
        cloned_net.set_input_record(inputs)
    return cloned_net, blob_remap
