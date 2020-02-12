import ubermagutil.units as uu


def test_multiplier():
    tol = 1e-6
    assert uu.si_multiplier(1e-9) == 1e-9
    assert uu.si_multiplier(50e-9) == 1e-9
    assert uu.si_multiplier(100e-9) == 1e-9
    assert uu.si_multiplier(1001e-9) == 1e-6
    assert uu.si_multiplier(0) == 1
    assert uu.si_multiplier(1e3) == 1e3
    assert uu.si_multiplier(0.5e-9) == 1e-12
    assert uu.si_multiplier(0.5) == 1e-3
    assert uu.si_multiplier(0.05) == 1e-3
    assert uu.si_multiplier(5) == 1
    assert uu.si_multiplier(50) == 1
    assert uu.si_multiplier(500) == 1
    assert uu.si_multiplier(5e30) is None


def test_si_max_multiplier():
    values = (5e-10, 6e-09, 4e-09)
    assert uu.si_max_multiplier(values) == 1e-9
    values = (1, 1e-3, 1e-6)
    assert uu.si_max_multiplier(values) == 1
    values = (1, 1e3, 1e6)
    assert uu.si_max_multiplier(values) == 1e6
