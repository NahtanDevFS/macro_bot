from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Action(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass