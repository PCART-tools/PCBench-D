def get_user_object_from_id(obj_id):
    obj = user_obj_id_to_weakref[obj_id]()
    assert obj is not None, "User object is no longer alive"
    return obj
