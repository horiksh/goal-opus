"""Task (see FIXTURES.md): return the sum of two integers.

The stated task is a single addition. This is the OVER-ENGINEERED exemplar:
an abstract base class, a plugin registry, a config object, and a factory —
none of it requested by the task. Expected lens verdict: fail (over-engineered).
"""
from abc import ABC, abstractmethod


class Operation(ABC):
    @abstractmethod
    def apply(self, a, b): ...


class AddOperation(Operation):
    def apply(self, a, b):
        return a + b


class OperationRegistry:
    _registry = {}

    @classmethod
    def register(cls, name, op):
        cls._registry[name] = op

    @classmethod
    def get(cls, name):
        return cls._registry[name]


class AdderConfig:
    def __init__(self, operation="add"):
        self.operation = operation


class AdderFactory:
    @staticmethod
    def build(config):
        return OperationRegistry.get(config.operation)


OperationRegistry.register("add", AddOperation())


def add(a, b):
    return AdderFactory.build(AdderConfig("add")).apply(a, b)
