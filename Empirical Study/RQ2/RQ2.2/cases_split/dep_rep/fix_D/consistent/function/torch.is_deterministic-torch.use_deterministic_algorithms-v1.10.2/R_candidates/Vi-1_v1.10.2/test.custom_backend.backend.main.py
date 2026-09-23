def main():
    parser = argparse.ArgumentParser(
        description="Lower a Module to a custom backend"
    )
    parser.add_argument("--export-module-to", required=True)
    options = parser.parse_args()

    # Load the library containing the custom backend.
    library_path = get_custom_backend_library_path()
    torch.ops.load_library(library_path)
    assert library_path in torch.ops.loaded_libraries

    # Lower an instance of Model to the custom backend  and export it
    # to the specified location.
    lowered_module = to_custom_backend(torch.jit.script(Model()))
    torch.jit.save(lowered_module, options.export_module_to)
