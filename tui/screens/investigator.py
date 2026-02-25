from rich.syntax import Syntax
from rich.table import Table
from textual.screen import Screen
from textual.widgets import RichLog, Input, Static
from textual.containers import Horizontal
import asyncio
from textual import work
from textual.app import ComposeResult

class InvestigatorScreen(Screen):
    def compose(self) -> ComposeResult:
        with Horizontal(id="agent_header"):
            yield Static("IDLE", id="status_idle", classes="status-indicator state-idle")
            yield Static("THINKING", id="status_thinking", classes="status-indicator state-thinking")
            yield Static("EXECUTING", id="status_executing", classes="status-indicator state-executing")
        
        yield RichLog(id="agent_log", max_lines=1000, auto_scroll=True)
        yield Input(placeholder="Send hint to Agent...", id="cmd_input")

    def on_mount(self) -> None:
        # Start the log streamer
        self.set_timer(1.0, self.log_streamer)

    @work(exclusive=True)
    async def log_streamer(self) -> None:
        log_view = self.query_one("#agent_log")
        counter = 0
        while True:
            # Simulate fetching logs
            # In a real implementation, this would call self.app.api.fetch_logs()
            
            # Add some sample log entries
            if counter % 5 == 0:
                # Simulate SSH command
                t = Table(show_header=False, box=None)
                t.add_row(f"[2026-02-14 10:30:{counter:02d}]", f"[cyan]sre-agent[/]", Syntax("df -h", "bash"))
                log_view.write(t)
            else:
                # Simulate brain activity
                log_view.write(f"[yellow][BRAIN][/] Analyzing system state, iteration {counter}")
            
            counter += 1
            await asyncio.sleep(2)

    def on_input_submitted(self, event: Input.Submitted):
        """Handle input submission."""
        # In a real implementation, this would call self.app.api.send_agent_hint(event.value)
        log_view = self.query_one("#agent_log")
        log_view.write(f"[blue][USER][/] {event.value}")

        # Clear the input
        self.query_one(Input).value = ""

    def on_mount(self) -> None:
        # Start the log streamer
        self.set_timer(1.0, self.log_streamer)