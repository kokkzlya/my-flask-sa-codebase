from abc import ABC, abstractmethod


class IHealthCheck(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError("TODO")
