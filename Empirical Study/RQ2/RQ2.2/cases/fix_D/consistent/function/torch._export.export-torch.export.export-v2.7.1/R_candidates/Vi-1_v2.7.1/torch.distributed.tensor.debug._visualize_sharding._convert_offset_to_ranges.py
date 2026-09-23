def _convert_offset_to_ranges(all_offsets):
    """
    Using tabulate package to create a table is easier when we specify row and col ranges
    This function converts offsets to ranges.
    """
    converted_blocks = []

    for offset in all_offsets:
        shape, offset, value = offset

        # Calculate row_range and column_range
        row_range = (offset[0], offset[0] + shape[0] - 1)
        column_range = (offset[1], offset[1] + shape[1] - 1)

        # Convert value to string to match your desired format
        converted_block = {
            "row_range": row_range,
            "column_range": column_range,
            "value": str(value),
        }
        converted_blocks.append(converted_block)

    return converted_blocks
