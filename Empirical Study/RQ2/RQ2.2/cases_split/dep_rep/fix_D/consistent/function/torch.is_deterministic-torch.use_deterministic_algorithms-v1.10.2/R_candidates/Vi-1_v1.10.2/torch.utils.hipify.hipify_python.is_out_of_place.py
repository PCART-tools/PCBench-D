def is_out_of_place(filepath):
    if filepath.startswith("torch/"):
        return False
    if filepath.startswith("tools/autograd/templates/"):
        return False
    return True
