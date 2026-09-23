def process_arg_list(arg_list):
    if arg_list == 'None':
        return None

    return [fr.strip() for fr in arg_list.split(',') if len(fr.strip()) > 0]
