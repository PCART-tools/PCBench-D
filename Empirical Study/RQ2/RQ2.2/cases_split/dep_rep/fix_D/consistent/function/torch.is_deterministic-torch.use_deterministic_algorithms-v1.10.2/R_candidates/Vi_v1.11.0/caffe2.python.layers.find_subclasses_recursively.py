def find_subclasses_recursively(base_cls, sub_cls):
    cur_sub_cls = base_cls.__subclasses__()
    sub_cls.update(cur_sub_cls)
    for cls in cur_sub_cls:
        find_subclasses_recursively(cls, sub_cls)
