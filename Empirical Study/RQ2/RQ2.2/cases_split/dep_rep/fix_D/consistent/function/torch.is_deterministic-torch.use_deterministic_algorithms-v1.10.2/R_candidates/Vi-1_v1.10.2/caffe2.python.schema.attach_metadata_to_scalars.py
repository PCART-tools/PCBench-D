def attach_metadata_to_scalars(field, metadata):
    for f in field.all_scalars():
        f.set_metadata(metadata)
