"""
Minimal working example to diagnose the empty interface issue
"""
from textual.app import App
from textual.widgets import Header, Footer, Label, Static
from textual.containers import Vertical
from textual.screen import Screen

class TestScreen(Screen):
    def compose(self):
        yield Vertical(
            Label("TEST SCREEN"),
            Static("This is a test screen to see if the interface renders"),
            Label("If you see this, the interface is working!")
        )

class MinimalTestApp(App):
    TITLE = "DeckForge - Minimal Test"
    
    def compose(self):
        yield Header()
        yield TestScreen(id="test")
        yield Footer()

if __name__ == "__main__":
    app = MinimalTestApp()
    app.run()