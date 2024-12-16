from abc import ABC, abstractmethod
class Machine(ABC):
    """Base class for all machines."""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def start(self):
        """Start the machine."""
        pass