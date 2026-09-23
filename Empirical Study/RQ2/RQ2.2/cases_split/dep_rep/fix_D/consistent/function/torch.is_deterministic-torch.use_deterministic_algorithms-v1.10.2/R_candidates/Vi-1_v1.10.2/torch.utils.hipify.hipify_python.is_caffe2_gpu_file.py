def is_caffe2_gpu_file(filepath):
    if filepath.startswith("c10/cuda"):
        return True
    filename = os.path.basename(filepath)
    _, ext = os.path.splitext(filename)
    return ('gpu' in filename or ext in ['.cu', '.cuh']) and ('cudnn' not in filename)
