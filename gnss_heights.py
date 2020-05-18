from math import sqrt


def htchk(metric, imperial):
    imp2metric = imperial * (1 / 3.28)
    msrdiff = round(metric - imp2metric, 5)
    return msrdiff


def bon2bam(bon):
    return sqrt(bon ** 2 - 0.16891 ** 2) - 0.04434
