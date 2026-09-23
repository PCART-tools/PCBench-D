def serialize_module_json_to_file(fx_module: GraphModule, fname: str):
    weights: Dict = {}
    serialized_json = json.dumps(serialize_module(fx_module, weights), indent=2)
    with open(fname, "w") as ofile:
        ofile.write(serialized_json)
