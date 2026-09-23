def main():
    parser = argparse.ArgumentParser(
        description="Serialize a script module with custom ops"
    )
    parser.add_argument("--export-script-module-to", required=True)
    options = parser.parse_args()

    torch.ops.load_library(get_custom_op_library_path())

    model = Model()
    model.save(options.export_script_module_to)
