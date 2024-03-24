from abc import ABC, ABCMeta, abstractmethod


class ServiceBase(ABC, metaclass=ABCMeta):
    _instance = None

    def __init__(self):
        pass

    @classmethod
    def get_singleton(cls):
        if cls._instance is None:
            cls._instance = cls.create_singleton()
        return cls._instance

    @classmethod
    @abstractmethod
    def create_singleton(cls):
        pass
