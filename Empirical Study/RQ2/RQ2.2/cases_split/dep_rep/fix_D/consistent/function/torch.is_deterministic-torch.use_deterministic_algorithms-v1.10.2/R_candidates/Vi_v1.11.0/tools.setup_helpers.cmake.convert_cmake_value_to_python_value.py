def convert_cmake_value_to_python_value(cmake_value: str, cmake_type: str) -> CMakeValue:
    r"""Convert a CMake value in a string form to a Python value.

    Args:
      cmake_value (string): The CMake value in a string form (e.g., "ON", "OFF", "1").
      cmake_type (string): The CMake type of :attr:`cmake_value`.

    Returns:
      A Python value corresponding to :attr:`cmake_value` with type :attr:`cmake_type`.
    """

    cmake_type = cmake_type.upper()
    up_val = cmake_value.upper()
    if cmake_type == 'BOOL':
        # https://gitlab.kitware.com/cmake/community/wikis/doc/cmake/VariablesListsStrings#boolean-values-in-cmake
        return not (up_val in ('FALSE', 'OFF', 'N', 'NO', '0', '', 'NOTFOUND') or up_val.endswith('-NOTFOUND'))
    elif cmake_type == 'FILEPATH':
        if up_val.endswith('-NOTFOUND'):
            return None
        else:
            return cmake_value
    else:  # Directly return the cmake_value.
        return cmake_value
