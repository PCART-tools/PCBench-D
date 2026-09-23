def dump():
    """Store the current runtime db state to the module file."""
    current_file = inspect.getfile(dump)
    f = open(current_file)
    current_content = f.read()
    f.close()
    begin_data_str = "# BEGIN GENERATED DATA\n"
    begin_data_index = current_content.find(begin_data_str)
    end_data_index = current_content.find("    # END GENERATED DATA\n")
    if begin_data_index == -1 or end_data_index == -1:
        warnings.warn(
            f"{current_file} cannot be updated:"
            " BEGIN/END GENERATED DATA comment blocks appear to be corrupted"
        )
        return

    def sort_key(key):
        op, device_name, version = key
        version = tuple(
            (str(item) if isinstance(item, torch.dtype) else item) for item in version
        )
        return (op, device_name, version)

    part1 = current_content[: begin_data_index + len(begin_data_str)]
    part2 = current_content[end_data_index:]
    data_part = []
    for op_key in sorted(_operation_device_version_data, key=sort_key):
        data_part.append("    " + repr(op_key).replace("'", '"') + ": {")
        op_data = _operation_device_version_data[op_key]
        data_part.extend(f"        {key}: {op_data[key]}," for key in sorted(op_data))
        data_part.append("    },")
    new_content = part1 + "\n".join(data_part) + "\n" + part2
    if current_content != new_content:
        f = open(current_file, "w")
        f.write(new_content)
        f.close()
