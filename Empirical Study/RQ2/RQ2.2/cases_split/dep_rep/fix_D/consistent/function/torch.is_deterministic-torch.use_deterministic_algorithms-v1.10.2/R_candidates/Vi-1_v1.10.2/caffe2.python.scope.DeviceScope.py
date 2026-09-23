@contextlib.contextmanager
def DeviceScope(scope, node_name=None):
    new_scope = caffe2_pb2.DeviceOption()
    if scope:
        assert isinstance(scope, caffe2_pb2.DeviceOption), \
            "DeviceScope takes in a caffe2_pb2.DeviceOption as its argument."
        new_scope.CopyFrom(scope)
    else:
        assert node_name, "At least one argument should be non-null in DeviceScope"

    # rewrite node_name if it is explicitly given
    if node_name:
        new_scope.node_name = node_name
    global _threadlocal_scope
    old_scope = CurrentDeviceScope()
    # nested scope should inherit the node_name if it is not explicitly set
    if old_scope and old_scope.HasField('node_name') and \
            not new_scope.HasField('node_name'):
        new_scope.node_name = old_scope.node_name

    # nested scope should inherit the extra_info and merged it with new extra_info
    if old_scope and hasattr(old_scope, 'extra_info'):
        new_scope.extra_info.extend(old_scope.extra_info)
    new_scope.extra_info.sort()

    _threadlocal_scope.devicescope = new_scope
    try:
        yield
    finally:
        assert _threadlocal_scope.devicescope == new_scope, \
            "The device scope is changed from outside DeviceScope() calls."
        _threadlocal_scope.devicescope = old_scope
