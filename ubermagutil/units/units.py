import collections


si_prefixes = collections.OrderedDict({'y': 1e-24,  # yocto
                                       'z': 1e-21,  # zepto
                                       'a': 1e-18,  # atto
                                       'f': 1e-15,  # femto
                                       'p': 1e-12,  # pico
                                       'n': 1e-9,   # nano
                                       'u': 1e-6,   # micro
                                       'm': 1e-3,   # mili
                                       '':  1,      # no prefix
                                       'k': 1e3,    # kilo
                                       'M': 1e6,    # mega
                                       'G': 1e9,    # giga
                                       'T': 1e12,   # tera
                                       'P': 1e15,   # peta
                                       'E': 1e18,   # exa
                                       'Z': 1e21,   # zetta
                                       'Y': 1e24})  # yotta
rsi_prefixes = {v: k for k, v in si_prefixes.items()}


def si_multiplier(value):
    """Determines SI multiplier.

    SI multiplier of :math:`x` is considered to be a value :math:`m=10^{n}`,
    for :math:`n = ..., -6, -3, 0, 3, 6,...`, for which :math:`1 \\le x/m
    < 10^{3}`.

    Parameters
    ----------
    value : numbers.Real

        Value for which the multiplier is computed.

    Returns
    -------
    float

        Multiplier as :math:`10^{n}`. If multiplier cannot be found, ``None``
        is returned.

    Examples
    --------
    1. Find a multiplier.

    >>> import ubermagutil.units as uu
    ...
    >>> uu.si_multiplier(5e-9)  # value on a nanoscale
    1e-09
    >>> uu.si_multiplier(500e-6)  # value on a microscale
    1e-06
    >>> uu.si_multiplier(0.5e-9)  # value on a picoscale
    1e-12

    .. seealso:: :py:class:`~ubermagutil.units.si_max_multiplier`

    """
    if value == 0:
        return 1
    else:
        for prefix, multiplier in reversed(si_prefixes.items()):
            if 1 <= value / multiplier < 1e3:
                return multiplier
        else:
            return None


def si_max_multiplier(values):
    """Determines maximum SI multiplier for a list of values.

    SI multiplier is computed for all elements of ``values`` using
    ``ubermagutil.units.si_multiplier`` and the largest one is returned.

    Parameters
    ----------
    values : list of numbers.Real

        Values for which the maximum multiplier is computed.

    Returns
    -------
    float

        Multiplier as :math:`10^{n}`. If multiplier cannot be found, ``None``
        is returned.

    Examples
    --------
    1. Find a maximum multiplier.

    >>> import ubermagutil.units as uu
    ...
    >>> uu.si_max_multiplier([5e-9, 50e-9, 500e-9, 5000e-9])
    1e-06
    >>> uu.si_max_multiplier([500e-6, 1])
    1
    >>> uu.si_max_multiplier([500e-12, 1e-11])
    1e-12

    .. seealso:: :py:class:`~ubermagutil.units.si_multiplier`

    """
    return max(list(map(si_multiplier, values)))
