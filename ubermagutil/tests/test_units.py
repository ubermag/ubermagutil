import ubermagutil.units as uu


def test_multiplier():
    tol = 1e-6
    assert (uu.si_multiplier(1e-9)[0] - 1) < tol
    assert uu.si_multiplier(1e-9)[1] == 'n'
    assert (uu.si_multiplier(50e-9)[0] - 50) < tol
    assert uu.si_multiplier(50e-9)[1] == 'n'
    assert (uu.si_multiplier(100e-9)[0] - 100) < tol
    assert uu.si_multiplier(100e-9)[1] == 'n'
    assert (uu.si_multiplier(1001e-9)[0] - 1.001) < tol
    assert uu.si_multiplier(1001e-9)[1] == 'u'
    assert (uu.si_multiplier(0)[0] - 0) < tol
    assert uu.si_multiplier(0)[1] == ''
    assert (uu.si_multiplier(1e3)[0] - 1) < tol
    assert uu.si_multiplier(1e3)[1] == 'k'
    assert (uu.si_multiplier(0.5e-9)[0] - 500) < tol
    assert uu.si_multiplier(0.5e-9)[1] == 'p'
    assert (uu.si_multiplier(0.5)[0] - 500) < tol
    assert uu.si_multiplier(0.5)[1] == 'm'
    assert (uu.si_multiplier(0.05)[0] - 50) < tol
    assert uu.si_multiplier(0.05)[1] == 'm'
    assert (uu.si_multiplier(5)[0] - 5) < tol
    assert uu.si_multiplier(5)[1] == ''
    assert (uu.si_multiplier(50)[0] - 50) < tol
    assert uu.si_multiplier(50)[1] == ''
    assert (uu.si_multiplier(500)[0] - 500) < tol
    assert uu.si_multiplier(500)[1] == ''
