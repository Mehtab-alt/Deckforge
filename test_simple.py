from textual.app import App
from textual.widgets import Label

class TestApp(App):
    def compose(self):
        yield Label("Test")

if __name__ == "__main__":
    app = TestApp()
    print("Simple app created successfully")