def shrink_output_schema(net, out_schema):
    if len(out_schema.field_names()) <= 1:
        return out_schema
    exists = [net.BlobIsDefined(blob) for blob in out_schema.field_blobs()]
    return schema.from_column_list(
        [
            col_name for ok, col_name in
            zip(exists, out_schema.field_names()) if ok
        ],
        [
            col_type for ok, col_type in
            zip(exists, out_schema.field_types()) if ok
        ],
        [
            col_blob for ok, col_blob in
            zip(exists, out_schema.field_blobs()) if ok
        ],
        [
            col_meta for ok, col_meta in
            zip(exists, out_schema.field_metadata()) if ok
        ]
    )
