from src.calculator import TriangleCalculator
from src.database import TriangleDatabase
from src.user_interface import ConsoleUserInterface
from src.external_service import ServerService
from src.controller import Controller


calculator = TriangleCalculator()
database = TriangleDatabase()
user_interface = ConsoleUserInterface()
external_service = ServerService()

controller = Controller(
    calculator,
    database,
    user_interface,
    external_service
)

result = controller.run()

print("Результат:", result)

database.connection.close()