class Controller:

    def __init__(
        self,
        calculator,
        database,
        user_interface,
        external_service
    ):
        self.calculator = calculator
        self.database = database
        self.user_interface = user_interface
        self.external_service = external_service

    def run(self):
        side_a, side_b, side_c = self.user_interface.get_data()

        record = self.database.get(
            side_a,
            side_b,
            side_c
        )

        if record is None:
            triangle_type, error_message = (
                self.calculator.calculate_triangle(
                    side_a,
                    side_b,
                    side_c
                )
            )

            self.database.add(
                side_a,
                side_b,
                side_c,
                triangle_type,
                error_message
            )

        else:
            triangle_type = record[3]
            error_message = record[4]

        if error_message:
            result = error_message
        else:
            result = triangle_type

        self.external_service.send(result)

        return result