import pytest
import joommfutil.typesystem as ts


def test_typesystem():
    @ts.typesystem(a=ts.Real,
                   b=ts.Int,
                   c=ts.String,
                   d=ts.UnsignedReal,
                   e=ts.PositiveReal,
                   f=ts.Vector,
                   g=ts.SizedVector(size=2),
                   h=ts.RealVector(size=3),
                   i=ts.PositiveRealVector(size=3),
                   j=ts.TypedAttribute(expected_type=dict),
                   k=ts.ObjectName,
                   l=ts.IntVector(size=3),
                   m=ts.PositiveIntVector(size=3),
                   n=ts.FromSet(allowed_values={1, 2, "b"}))
    class DummyClass:
        def __init__(self, a, b, c, d, e, f, g, h, i, j, k, l, m, n):
            self.a = a
            self.b = b
            self.c = c
            self.d = d
            self.e = e
            self.f = f
            self.g = g
            self.h = h
            self.i = i
            self.j = j
            self.k = k
            self.l = l
            self.m = m
            self.n = n

    a = 1.7
    b = 2
    c = "abc"
    d = 9.5
    e = 11.
    f = (1, 3, -4, 9)
    g = (1, 2)
    h = (-1, 2, 3.1)
    i = (1, 2, 31.1)
    j = {}
    k = "exchange_energy_name"
    l = (-1, 2, -3)
    m = (1, 2, 3)
    n = 1

    dc = DummyClass(a=a, b=b, c=c, d=d, e=e, f=f, g=g,
                    h=h, i=i, j=j, k=k, l=l, m=m, n=n)

    # Simple assertions
    assert dc.a == a
    assert dc.b == b
    assert dc.c == c
    assert dc.d == d
    assert dc.e == e
    assert dc.f == f
    assert dc.g == g
    assert dc.h == h
    assert dc.i == i
    assert dc.j == j
    assert dc.k == k
    assert dc.l == l
    assert dc.m == m
    assert dc.n == n

    # Valid settings
    dc.a = 77.4
    assert dc.a == 77.4
    dc.b = -77
    assert dc.b == -77
    dc.c = "dummystring"
    assert dc.c == "dummystring"
    dc.d = 61.2
    assert dc.d == 61.2
    dc.e = 0.1
    assert dc.e == 0.1
    dc.f = [1, 2, 3, 4, 5, 6.1]
    assert dc.f == [1, 2, 3, 4, 5, 6.1]
    dc.g = (3, 2.1)
    assert dc.g == (3, 2.1)
    dc.h = (-5, 6, 8)
    assert dc.h == (-5, 6, 8)
    dc.i = (1, 2, 3.2)
    assert dc.i == (1, 2, 3.2)
    dc.j = {"a": 1}
    assert dc.j == {"a": 1}
    dc.k = "_new_name2"
    assert dc.k == "_new_name2"
    dc.l = (-11, -5, 6)
    assert dc.l == (-11, -5, 6)
    dc.m = (5, 9, 879)
    assert dc.m == (5, 9, 879)
    dc.n = "b"
    assert dc.n == "b"

    # Invalid settings
    with pytest.raises(TypeError):
        dc.a = 1+2j
    with pytest.raises(TypeError):
        dc.b = -77.1
    with pytest.raises(TypeError):
        dc.c = 5
    with pytest.raises(TypeError):
        dc.d = -61.2
    with pytest.raises(TypeError):
        dc.e = -0.1
    with pytest.raises(TypeError):
        dc.f = "abc"
    with pytest.raises(TypeError):
        dc.g = (3, 2.1, -6)
    with pytest.raises(TypeError):
        dc.h = (-5, 6, 8, 9)
    with pytest.raises(TypeError):
        dc.h = (-5+1j, 8, 9)
    with pytest.raises(TypeError):
        dc.i = (1, -2, 3.2)
    with pytest.raises(TypeError):
        dc.j = 5
    with pytest.raises(TypeError):
        dc.k = "new name2"
    with pytest.raises(TypeError):
        dc.k = "2newname2"
    with pytest.raises(TypeError):
        dc.l = (1.1, 2, 5)
    with pytest.raises(TypeError):
        dc.m = (0, 2, 5)
    with pytest.raises(TypeError):
        dc.n = -25

    # Attempt deleting attribute
    with pytest.raises(AttributeError):
        del dc.i


def test_missing_size_option():
    with pytest.raises(TypeError):
        @ts.typesystem(a=ts.SizedVector)
        class DummyClass:
            def __init__(self, a):
                self.a = a


def test_missing_expected_type_option():
    with pytest.raises(TypeError):
        @ts.typesystem(a=ts.TypedAttribute)
        class DummyClass:
            def __init__(self, a):
                self.a = a


def test_missing_allowed_values_option():
    with pytest.raises(TypeError):
        @ts.typesystem(a=ts.FromSet)
        class DummyClass:
            def __init__(self, a):
                self.a = a


def test_constanttypesystem():
    @ts.typesystem(a=ts.ConstantRealVector(size=3),
                   b=ts.ConstantPositiveRealVector(size=3),
                   c=ts.ConstantObjectName,
                   d=ts.ConstantFromSet(allowed_values={1, 2, -9}))
    class DummyClass:
        def __init__(self, a, b, c, d):
            self.a = a
            self.b = b
            self.c = c
            self.d = d

    a = (0, -1, 2.4)
    b = (1.2, 3.14, 5e-6)
    c = "object_name"
    d = 1

    dc = DummyClass(a=a, b=b, c=c, d=d)

    # Simple assertions
    assert dc.a == a
    assert dc.b == b
    assert dc.c == c
    assert dc.d == d

    # Attempt to change value.
    with pytest.raises(AttributeError):
        dc.a = (1, 0, 3)
    with pytest.raises(AttributeError):
        dc.b = (5, 6.1, 7)
    with pytest.raises(AttributeError):
        dc.c = "new_object_name"
    with pytest.raises(AttributeError):
        dc.d = -9

    # Attempt deleting attribute.
    with pytest.raises(AttributeError):
        del dc.a


def test_usecase():
    @ts.typesystem(a=ts.ConstantRealVector(size=3),
                   b=ts.ConstantPositiveRealVector(size=3),
                   c=ts.PositiveReal)
    class DummyClass:
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

    a1 = (5, 4, -6.1e-3)
    b1 = (0.1, 2, 3)
    c1 = 9
    dc1 = DummyClass(a=a1, b=b1, c=c1)

    a2 = (1, 1, -2)
    b2 = (9, 10, 12)
    c2 = 78
    dc2 = DummyClass(a=a2, b=b2, c=c2)

    assert dc1.a == a1
    assert dc1.b == b1
    assert dc1.c == c1

    assert dc2.a == a2
    assert dc2.b == b2
    assert dc2.c == c2

    # Attempt to change constant values
    with pytest.raises(AttributeError):
        dc1.a = (1, 0, 3)
    with pytest.raises(AttributeError):
        dc1.b = (5, 6.1, 7)
    with pytest.raises(AttributeError):
        dc2.a = (1, 0, 3)
    with pytest.raises(AttributeError):
        dc2.b = (5, 6.1, 7)

    # Change variable value
    dc1.c = 11

    # Assert values after changes
    assert dc1.a == a1
    assert dc1.b == b1
    assert dc1.c == 11

    assert dc2.a == a2
    assert dc2.b == b2
    assert dc2.c == c2

    # Attempt deleting attributes
    with pytest.raises(AttributeError):
        del dc1.a
    with pytest.raises(AttributeError):
        del dc1.b
    with pytest.raises(AttributeError):
        del dc1.c
    with pytest.raises(AttributeError):
        del dc2.a
    with pytest.raises(AttributeError):
        del dc2.b
    with pytest.raises(AttributeError):
        del dc2.c
