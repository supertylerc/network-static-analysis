# stdlib
import abc


class ParserBase(metaclass=abc.ABCMeta):
    def __init__(self):
        self.kind = "parser"
        self.name = type(self).__name__.lower().replace(self.kind, "")

    def setup(self):
        pass

    @abc.abstractmethod
    def parse(self, data):
        pass

    def teardown(self):
        pass


class InputBase(metaclass=abc.ABCMeta):
    def __init__(self):
        self.kind = "input"
        self.name = type(self).__name__.lower().replace(self.kind, "")

    def setup(self):
        pass

    @abc.abstractmethod
    def read(self, data):
        pass

    def teardown(self):
        pass


class OutputBase(metaclass=abc.ABCMeta):
    def __init__(self):
        self.kind = "input"
        self.name = type(self).__name__.lower().replace(self.kind, "")

    def setup(self):
        pass

    @abc.abstractmethod
    def write(self, data):
        pass

    def teardown(self):
        pass
