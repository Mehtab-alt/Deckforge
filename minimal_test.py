from textual.app import App
from textual.widgets import Label, Header, Footer
from textual.containers import Vertical, Horizontal

class MinimalApp(App):
    """A minimal app to test if Textual is working properly."""
    
    def compose(self):
        yield Header()
        yield Vertical(
            Label("DeckForge TUI - Minimal Test"),
            Label("If you see this, Textual is working"),
            Label("Press Ctrl+C to exit")
        )
        yield Footer()

if __name__ == "__main__":
    app = MinimalApp()
    app.run()