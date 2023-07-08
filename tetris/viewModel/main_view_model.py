from ..model.reactive_model import ReactiveModel


class MainViewModel(ReactiveModel):
    state: str
    complexity: int
    command: str

    def set_state(self, state: str):
        self.state = state

    def set_complexity(self, complexity: int):
        self.complexity = complexity

    def set_command(self, app_model_command: str):
        self.command = app_model_command


app_model = MainViewModel()
app_model.state = "menu"
