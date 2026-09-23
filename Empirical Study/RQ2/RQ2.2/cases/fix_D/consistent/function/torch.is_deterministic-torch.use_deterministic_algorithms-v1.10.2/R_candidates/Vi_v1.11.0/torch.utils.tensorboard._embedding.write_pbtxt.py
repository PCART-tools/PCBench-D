def write_pbtxt(save_path, contents):
    fs = tf.io.gfile.get_filesystem(save_path)
    config_path = fs.join(save_path, 'projector_config.pbtxt')
    fs.write(config_path, tf.compat.as_bytes(contents), binary_mode=True)
