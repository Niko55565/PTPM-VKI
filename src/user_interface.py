from abc import ABC, abstractmethod


class UserInterface(ABC):

    @abstractmethod
    def get_data(self):
        """Получение данных пользователя."""


class ConsoleUserInterface(UserInterface):

    def get_data(self):
        side_a = input("Введите сторону A: ")
        side_b = input("Введите сторону B: ")
        side_c = input("Введите сторону C: ")

        return side_a, side_b, side_c