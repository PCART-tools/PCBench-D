def _mesh_to_coordinate(mesh, device_type):
    """
    Given a n-dimensional list of device mesh, this function creates a map of
    device and its coordinate
    """
    # Convert the n-dimensional list to a NumPy array
    np_mesh = np.array(mesh.mesh.tolist())

    # Create a dictionary to map each value to its coordinate
    device_to_coordinate_map = {}
    for coord, value in np.ndenumerate(np_mesh):
        # device is unique in device_mesh
        device_to_coordinate_map[f"{device_type}:{str(value)}"] = list(coord)

    return device_to_coordinate_map
