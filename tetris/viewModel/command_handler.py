from ..base.ICommand import ICommand


class CommandHandler:
    def __init__(self):
        self.history: list[ICommand] = []

    def add_command(self, command: ICommand) -> None:
        self.history.append(command)

    def execute_commands(self):
        if not self.history:
            print("No commands to execute")
        else:
            for executor in self.history:
                executor.execute()
        self.history.clear()


command_handler = CommandHandler()
