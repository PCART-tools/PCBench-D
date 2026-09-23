def remove_build_path():
    if sys.platform == "win32":
        print("Not wiping extensions build folder because Windows")
        return
    default_build_root = torch.utils.cpp_extension.get_default_build_root()
    if os.path.exists(default_build_root):
        shutil.rmtree(default_build_root)
