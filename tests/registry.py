# -*- coding: utf-8 -*-


from makeyfile.register import MakeyfileRegistry


def test_registry_defaults():
    registry = MakeyfileRegistry()
    assert "runner" in registry
    assert isinstance(registry["runner"], dict)
    assert list(registry) == ["runner"]
    assert registry["runner"].keys() == ['sequence', 'python', 'shell']


def test_registry_register():

    class FooClass(object):
        pass

    class BarClass(object):
        pass

    foo = FooClass()
    bar = BarClass()

    registry = MakeyfileRegistry()
    registry.register('cat1', "foo", foo)
    assert list(registry) == ["runner", "cat1"]
    registry["cat1"].keys() == ["foo"]
    assert registry["cat1"]["foo"] is foo

    registry.register('cat1', "bar", bar)
    assert list(registry) == ["runner", "cat1"]
    registry["cat1"].keys() == ["bar"]
    assert registry["cat1"]["bar"] is bar

    registry.register('cat2', "foo", foo)
    assert list(registry) == ["runner", "cat1", "cat2"]
    registry["cat2"].keys() == ["foo"]
    assert registry["cat2"]["foo"] is foo
