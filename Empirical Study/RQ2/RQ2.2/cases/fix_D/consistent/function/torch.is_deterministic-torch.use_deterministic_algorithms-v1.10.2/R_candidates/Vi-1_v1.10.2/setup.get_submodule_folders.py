def get_submodule_folders():
    git_modules_path = os.path.join(cwd, ".gitmodules")
    default_modules_path = [os.path.join(third_party_path, name) for name in [
                            "gloo", "cpuinfo", "tbb", "onnx",
                            "foxi", "QNNPACK", "fbgemm"
                            ]]
    if not os.path.exists(git_modules_path):
        return default_modules_path
    with open(git_modules_path) as f:
        return [os.path.join(cwd, line.split("=", 1)[1].strip()) for line in
                f.readlines() if line.strip().startswith("path")]
