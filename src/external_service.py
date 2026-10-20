from abc import ABC, abstractmethod


class ExternalService(ABC):

    @abstractmethod
    def send(self, message):
        """Отправка данных стороннему сервису."""


class ServerService(ExternalService):

    def send(self, message):
        print(f"Отправка на внешний сервер: {message}")