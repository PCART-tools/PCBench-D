def is_caffe2_gpu_file(rel_filepath):
    assert not os.path.isabs(rel_filepath)
    if rel_filepath.startswith("c10/cuda"):
        return True
    filename = os.path.basename(rel_filepath)
    _, ext = os.path.splitext(filename)
    return ('gpu' in filename or ext in ['.cu', '.cuh']) and ('cudnn' not in filename)
