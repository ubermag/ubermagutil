import pytest

import ubermagutil as uu


def test_hysteresis_values():
    res = uu.hysteresis_values(-1, 1, 1)
    assert isinstance(res, list)
    assert len(res) == 5
    assert abs(res[0] - 1) < 1e-6
    assert abs(res[-1] - 1) < 1e-6
    assert (res[1] - res[0] - 1) < 1e-6

    res = uu.hysteresis_values(-1e6, 1e6, 0.1e6)
    assert isinstance(res, list)
    assert len(res) == 41
    assert abs(res[0] - 1e6) < 1e-6
    assert abs(res[-1] - 1e6) < 1e-6
    assert (res[1] - res[0] - 0.1e6) < 1e-6

    res = uu.hysteresis_values(-1e-6, 1e-6, 0.01e-6)
    assert isinstance(res, list)
    assert len(res) == 401
    assert abs(res[0] - 1e-6) < 1e-9
    assert abs(res[-1] - 1e-6) < 1e-9
    assert (res[1] - res[0] - 0.01e-6) < 1e-9

    # Exception
    with pytest.raises(ValueError):
        uu.hysteresis_values(-1, 1, 0.3)
