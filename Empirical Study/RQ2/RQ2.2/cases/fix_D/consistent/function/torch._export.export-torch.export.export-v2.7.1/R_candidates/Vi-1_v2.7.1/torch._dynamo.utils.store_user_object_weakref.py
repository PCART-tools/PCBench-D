def store_user_object_weakref(obj):
    obj_id = id(obj)
    user_obj_id_to_weakref[obj_id] = weakref.ref(obj)
