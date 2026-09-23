def make_tsv(metadata, save_path, metadata_header=None):
    if not metadata_header:
        metadata = [str(x) for x in metadata]
    else:
        assert len(metadata_header) == len(metadata[0]), \
            'len of header must be equal to the number of columns in metadata'
        metadata = ['\t'.join(str(e) for e in l)
                    for l in [metadata_header] + metadata]

    metadata_bytes = tf.compat.as_bytes('\n'.join(metadata) + '\n')
    fs = tf.io.gfile.get_filesystem(save_path)
    fs.write(fs.join(save_path, 'metadata.tsv'), metadata_bytes, binary_mode=True)
