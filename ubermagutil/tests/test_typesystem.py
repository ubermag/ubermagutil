import pytest
import numbers
import numpy as np
import ubermagutil.typesystem as ts


@ts.typesystem(t1=ts.Typed(expected_type=int),
               t2=ts.Typed(expected_type=numbers.Real),
               t3=ts.Typed(expected_type=str),
               t4c=ts.Typed(expected_type=list, const=True),
               s1=ts.Scalar(),
               s2=ts.Scalar(expected_type=float),
               s3=ts.Scalar(positive=True),
               s4=ts.Scalar(unsigned=True, otherwise=str),
               s5=ts.Scalar(expected_type=int, positive=True),
               s6=ts.Scalar(expected_type=numbers.Real, positive=False),
               s7c=ts.Scalar(expected_type=float, unsigned=True, const=True),
               v1=ts.Vector(),
               v2=ts.Vector(size=5),
               v3=ts.Vector(unsigned=True),
               v4=ts.Vector(positive=True, otherwise=int),
               v5=ts.Vector(size=1, positive=False),
               v6=ts.Vector(component_type=int),
               v7=ts.Vector(size=3, component_type=float),
               v8c=ts.Vector(size=2, component_type=int, const=True),
               n1=ts.Name(),
               n2c=ts.Name(const=True),
               d1=ts.Dictionary(key_descriptor=ts.Name(),
                                value_descriptor=ts.Scalar(),
                                allow_empty=True),
               d2=ts.Dictionary(key_descriptor=ts.Scalar(),
                                value_descriptor=ts.Vector(size=3),
                                otherwise=str,
                                allow_empty=False),
               d3=ts.Dictionary(key_descriptor=ts.Name(),
                                value_descriptor=ts.Scalar()),
               d4c=ts.Dictionary(key_descriptor=ts.Name(),
                                 value_descriptor=ts.Typed(expected_type=str),
                                 const=True),
               ss1=ts.Subset(sample_set=set([1, 2, '5']), unpack=False),
               ss2=ts.Subset(sample_set=set([-1, 5]), unpack=False),
               ss3=ts.Subset(sample_set='xyz', unpack=True, otherwise=float),
               ss4c=ts.Subset(sample_set='abc', unpack=True, const=True),
               p1=ts.Parameter(),
               p2=ts.Parameter(descriptor=ts.Scalar(expected_type=int)),
               p3=ts.Parameter(descriptor=ts.Scalar(positive=True)),
               p4=ts.Parameter(descriptor=ts.Vector(size=3), otherwise=float),
               p5c=ts.Parameter(descriptor=ts.Scalar(), const=True))
class DecoratedClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def test_typed():
    dc = DecoratedClass()

    # Valid sets
    dc.t1 = -999
    dc.t2 = 3.1e6
    dc.t3 = ''
    dc.t4c = []

    # Exceptions
    with pytest.raises(TypeError):
        dc.t1 = 0.1
    with pytest.raises(TypeError):
        dc.t2 = {}
    with pytest.raises(TypeError):
        dc.t3 = 5
    with pytest.raises(AttributeError):
        dc.t4c = [1, 2]  # const attribute
    with pytest.raises(AttributeError):
        del dc.t1  # delete attribute

    # Is value affected?
    assert dc.t3 == ''


def test_scalar():
    dc = DecoratedClass(s2=3.3)

    # Valid sets
    dc.s1 = -1
    dc.s2 = -5.2
    dc.s3 = 1e-11
    dc.s4 = 101
    dc.s4 = 'ubermag'
    dc.s5 = 20
    dc.s6 = -500
    dc.s7c = 3.14

    # Exceptions
    with pytest.raises(TypeError):
        dc.s1 = []
    with pytest.raises(TypeError):
        dc.s2 = 5000
    with pytest.raises(ValueError):
        dc.s3 = 0
    with pytest.raises(ValueError):
        dc.s4 = -1.2
    with pytest.raises(TypeError):
        dc.s5 = -0.1  # Caught when checking type
    with pytest.raises(TypeError):
        dc.s6 = []
    with pytest.raises(AttributeError):
        dc.s7c = 1.2  # const attribute
    with pytest.raises(AttributeError):
        del dc.s2  # delete attribute

    # Is value affected?
    assert dc.s4 == 'ubermag'
    assert dc.s5 == 20


def test_vector():
    dc = DecoratedClass()

    # Valid sets
    dc.v1 = (1, 5e-9)
    dc.v2 = np.array([1, 2, 3, 0.1, -1e-9])
    dc.v3 = [1, 0]
    dc.v4 = np.array([5, 1e5])
    dc.v4 = 15  # otherwise int
    dc.v5 = (-5,)
    dc.v6 = [5, 9]
    dc.v7 = (11.1, np.pi, 0.0)
    dc.v8c = [1, 9]

    # Exceptions
    with pytest.raises(TypeError):
        dc.v1 = {}
    with pytest.raises(ValueError):
        dc.v2 = (20, 11, -13)
    with pytest.raises(ValueError):
        dc.v3 = [-1, 5]
    with pytest.raises(ValueError):
        dc.v4 = (9, -3)
    with pytest.raises(ValueError):
        dc.v5 = []
    with pytest.raises(TypeError):
        dc.v6 = ['a', 1, 3]
    with pytest.raises(TypeError):
        dc.v7 = [1.1, 2, np.pi]
    with pytest.raises(AttributeError):
        dc.v8c = [1, 55]  # const attribute
    with pytest.raises(AttributeError):
        del dc.v2  # delete attribute

    # Is value affected?
    assert dc.v5 == (-5,)


def test_name():
    dc = DecoratedClass(n1='var_name')

    # Valid sets
    dc.n1 = 'a1'
    dc.n1 = 'some_name'
    dc.n1 = 'a1a'
    dc.n2c = 'var_name123_2'

    # Exceptions
    with pytest.raises(TypeError):
        dc.n1 = 5
    with pytest.raises(ValueError):
        dc.n1 = '1a'
    with pytest.raises(ValueError):
        dc.n1 = '-a'
    with pytest.raises(ValueError):
        dc.n1 = 'var name'
    with pytest.raises(ValueError):
        dc.n1 = 'var-name'
    with pytest.raises(AttributeError):
        dc.n2c = 'ubermag'  # const attribute
    with pytest.raises(AttributeError):
        del dc.n2c  # delete attribute

    # Is value affected?
    assert dc.n1 == 'a1a'


def test_dictionary():
    dc = DecoratedClass()

    # Valid sets
    dc.d1 = {'a': 15, 'b': -51}  # Valid set
    dc.d1 = {}
    dc.d2 = {1: (1, 2, -3), -11: (0, 0, 0)}
    dc.d2 = 'ubermag'
    dc.d3 = {'a': -1e-9, 'b': 1e6}
    dc.d4c = {'r1': 'Southampton', 'r2': 'Hamburg'}

    # Exceptions
    with pytest.raises(TypeError):
        dc.d1 = 'a'
    with pytest.raises(TypeError):
        dc.d1 = {'a': 15, 'b': [1, 2, 3]}
    with pytest.raises(ValueError):
        dc.d2 = {}  # empty dictionary
    with pytest.raises(ValueError):
        dc.d3 = {}  # empty dictionary
    with pytest.raises(AttributeError):
        dc.d4c = {'r1': 'Hamburg', 'r2': 'London'}  # const attribute
    with pytest.raises(AttributeError):
        del dc.d2  # delete attribute

    # Is value affected?
    assert dc.d2 == 'ubermag'


def test_parameter():
    dc = DecoratedClass()

    # Valid sets
    dc.p2 = 1
    dc.p2 = {'r1': 2, 'r2': -15}
    dc.p3 = np.pi
    dc.p4 = np.pi  # otherwise float
    dc.p4 = (1, 2, 3)
    dc.p5c = {'a': 1.1, 'b': 2e-3}

    # Exceptions
    with pytest.raises(AttributeError):
        dc.p1 = -1.2  # descriptor not passed
    with pytest.raises(ValueError):
        dc.p2 = {}
    with pytest.raises(TypeError):
        dc.p3 = {1: 1, 'b': 5}
    with pytest.raises(ValueError):
        dc.p4 = {'string with spaces': (1, 2, 3)}
    with pytest.raises(AttributeError):
        dc.p5c = {'a': 1.2, 'b': 2.2e-3}  # const attribute
    with pytest.raises(AttributeError):
        del dc.p4

    # Is value affected?
    assert dc.p2 == {'r1': 2, 'r2': -15}
    assert dc.p4 == (1, 2, 3)


def test_subset():
    dc = DecoratedClass()

    # Valid sets
    dc.ss1 = '5'
    dc.ss2 = -1
    dc.ss3 = 'zzxy'
    dc.ss3 = 3.14
    dc.ss4c = 'cbacbaaab'

    # Exceptions
    with pytest.raises(ValueError):
        dc.ss1 = -1
    with pytest.raises(ValueError):
        dc.ss2 = 6
    with pytest.raises(ValueError):
        dc.ss3 = 'k'
    with pytest.raises(AttributeError):
        dc.ss4c = 'a'  # const attribute
    with pytest.raises(AttributeError):
        del dc.ss3  # delete attribute

    # Is value affected?
    assert dc.ss1 == '5'
    assert dc.ss2 == -1
    assert dc.ss3 == 3.14
    assert dc.ss4c == set('abc')
