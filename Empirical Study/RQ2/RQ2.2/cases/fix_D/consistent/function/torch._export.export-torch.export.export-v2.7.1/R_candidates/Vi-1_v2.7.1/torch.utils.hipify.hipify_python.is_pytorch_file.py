def is_pytorch_file(rel_filepath):
    assert not os.path.isabs(rel_filepath)
    if rel_filepath.startswith("aten/"):
        if rel_filepath.startswith("aten/src/ATen/core/"):
            return False
        return True
    if rel_filepath.startswith("torch/"):
        return True
    if rel_filepath.startswith("third_party/nvfuser/"):
        return True
    if rel_filepath.startswith("tools/autograd/templates/"):
        return True
    return False
