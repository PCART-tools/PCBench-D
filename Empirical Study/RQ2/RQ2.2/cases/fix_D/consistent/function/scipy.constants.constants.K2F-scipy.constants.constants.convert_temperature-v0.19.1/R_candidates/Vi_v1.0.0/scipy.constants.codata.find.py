def find(sub=None, disp=False):
    """
    Return list of physical_constant keys containing a given string.

    Parameters
    ----------
    sub : str, unicode
        Sub-string to search keys for.  By default, return all keys.
    disp : bool
        If True, print the keys that are found, and return None.
        Otherwise, return the list of keys without printing anything.

    Returns
    -------
    keys : list or None
        If `disp` is False, the list of keys is returned.
        Otherwise, None is returned.

    See Also
    --------
    codata : Contains the description of `physical_constants`, which, as a
        dictionary literal object, does not itself possess a docstring.

    Examples
    --------
    >>> from scipy.constants import find, physical_constants

    Which keys in the ``physical_constants`` dictionary contain 'boltzmann'?

    >>> find('boltzmann')
    ['Boltzmann constant',
     'Boltzmann constant in Hz/K',
     'Boltzmann constant in eV/K',
     'Boltzmann constant in inverse meters per kelvin',
     'Stefan-Boltzmann constant']

    Get the constant called 'Boltzmann constant in Hz/K':

    >>> physical_constants['Boltzmann constant in Hz/K']
    (20836612000.0, 'Hz K^-1', 12000.0)

    Find constants with 'radius' in the key:

    >>> find('radius')
    ['Bohr radius',
     'classical electron radius',
     'deuteron rms charge radius',
     'proton rms charge radius']
    >>> physical_constants['classical electron radius']
    (2.8179403227e-15, 'm', 1.9e-24)

    """
    if sub is None:
        result = list(_current_constants.keys())
    else:
        result = [key for key in _current_constants
                  if sub.lower() in key.lower()]

    result.sort()
    if disp:
        for key in result:
            print(key)
        return
    else:
        return result
