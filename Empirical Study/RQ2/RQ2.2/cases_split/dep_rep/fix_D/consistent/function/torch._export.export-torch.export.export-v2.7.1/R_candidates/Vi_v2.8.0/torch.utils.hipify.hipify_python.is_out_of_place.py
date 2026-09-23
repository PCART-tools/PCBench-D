def is_out_of_place(rel_filepath):
    assert not os.path.isabs(rel_filepath)
    if rel_filepath.startswith("torch/"):
        return False
    if rel_filepath.startswith("third_party/nvfuser/"):
        return False
    if rel_filepath.startswith("tools/autograd/templates/"):
        return False
    return True
