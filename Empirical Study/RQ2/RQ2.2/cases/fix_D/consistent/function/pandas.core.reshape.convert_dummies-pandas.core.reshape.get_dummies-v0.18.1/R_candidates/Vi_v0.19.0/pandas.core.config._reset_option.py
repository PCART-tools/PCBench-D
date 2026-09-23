def _reset_option(pat, silent=False):

    keys = _select_options(pat)

    if len(keys) == 0:
        raise OptionError('No such keys(s)')

    if len(keys) > 1 and len(pat) < 4 and pat != 'all':
        raise ValueError('You must specify at least 4 characters when '
                         'resetting multiple keys, use the special keyword '
                         '"all" to reset all the options to their default '
                         'value')

    for k in keys:
        _set_option(k, _registered_options[k].defval, silent=silent)
