def get_combined_dict(default_dict, additional_dict):
    d = default_dict.copy()
    d.update(additional_dict)
    return d
