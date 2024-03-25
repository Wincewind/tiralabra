import os

class ConsoleIO:
    def write(self, user_input):
        print(user_input)

    def read(self, prompt: str, expected_values: list):
        user_input = None
        while user_input not in expected_values:
            user_input = input(prompt)
            if user_input not in expected_values:
                os.system("cls")
                print(f"Valintaa '{user_input}' ei voida suorittaa")
        return user_input
