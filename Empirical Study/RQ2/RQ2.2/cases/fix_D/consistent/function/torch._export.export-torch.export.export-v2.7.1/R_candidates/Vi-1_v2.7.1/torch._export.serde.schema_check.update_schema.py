def update_schema():
    import importlib.resources

    if importlib.resources.is_resource(__package__, "schema.yaml"):
        content = importlib.resources.read_text(__package__, "schema.yaml")
        match = re.search("checksum<<([A-Fa-f0-9]{64})>>", content)
        _check(match is not None, "checksum not found in schema.yaml")
        assert match is not None
        checksum_head = match.group(1)

        thrift_content = importlib.resources.read_text(
            __package__, "export_schema.thrift"
        )
        match = re.search("checksum<<([A-Fa-f0-9]{64})>>", thrift_content)
        _check(match is not None, "checksum not found in export_schema.thrift")
        assert match is not None
        thrift_checksum_head = match.group(1)
        thrift_content = thrift_content.splitlines()
        assert thrift_content[0].startswith("// @" + "generated")
        assert thrift_content[1].startswith("// checksum<<")
        thrift_checksum_real = _hash_content("\n".join(thrift_content[2:]))

        from yaml import load, Loader

        dst = load(content, Loader=Loader)
        assert isinstance(dst, dict)
    else:
        checksum_head = None
        thrift_checksum_head = None
        thrift_checksum_real = None
        dst = {"SCHEMA_VERSION": None, "TREESPEC_VERSION": None}

    src, cpp_header, thrift_schema = _staged_schema()
    additions, subtractions = _diff_schema(dst, src)
    yaml_path = __package__.replace(".", "/") + "/schema.yaml"
    thrift_schema_path = __package__.replace(".", "/") + "/export_schema.thrift"
    torch_prefix = "torch/"
    assert yaml_path.startswith(torch_prefix)  # sanity check
    assert thrift_schema_path.startswith(torch_prefix)  # sanity check

    return _Commit(
        result=src,
        checksum_next=_hash_content(repr(src)),
        yaml_path=yaml_path,
        additions=additions,
        subtractions=subtractions,
        base=dst,
        checksum_head=checksum_head,
        cpp_header=cpp_header,
        cpp_header_path=torch_prefix + "csrc/utils/generated_serialization_types.h",
        thrift_checksum_head=thrift_checksum_head,
        thrift_checksum_real=thrift_checksum_real,
        thrift_checksum_next=_hash_content(thrift_schema),
        thrift_schema=thrift_schema,
        thrift_schema_path=thrift_schema_path,
    )
