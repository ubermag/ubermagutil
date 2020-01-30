import collections


si_prefixes = collections.OrderedDict({'y': 1e-24,  # yocto
                                       'z': 1e-21,  # zepto
                                       'a': 1e-18,  # atto
                                       'f': 1e-15,  # femto
                                       'p': 1e-12,  # pico
                                       'n': 1e-9,   # nano
                                       'u': 1e-6,   # micro
                                       'm': 1e-3,   # mili
                                       '' : 1,      # no prefix
                                       'k': 1e3,    # kilo
                                       'M': 1e6,    # mega
                                       'G': 1e9,    # giga
                                       'T': 1e12,   # tera
                                       'P': 1e15,   # peta
                                       'E': 1e18,   # exa
                                       'Z': 1e21,   # zetta
                                       'Y': 1e24})  # yotta

rsi_prefixes = {v : k for k, v in si_prefixes.items()}


def si_multiplier(value):
    if value == 0:
        multiplier = 1
        reduced_value = value
    else:
        for prefix, multiplier in reversed(si_prefixes.items()):
            reduced_value = value / multiplier
            if 1 <= reduced_value < 1e3:
                break

    return reduced_value, multiplier

def si_max_multiplier(values):
    return max(list(zip(*list(map(si_multiplier, values))))[1])
