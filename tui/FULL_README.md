# DeckForge Textual Interface (TUI) - Complete Implementation

This directory contains the complete Textual-based Terminal User Interface for the DeckForge platform, featuring a cyberpunk-inspired aesthetic and advanced SRE capabilities.

## Directory Structure

```
tui/
├── app.py                 # Main application entry point
├── bridge.py              # API communication layer
├── style.tcss             # Cyberpunk-themed styling (temporarily disabled due to CSS parsing issues)
├── screens/               # Individual screen implementations
│   ├── dashboard.py       # System telemetry dashboard
│   ├── forge_builder.py   # Infrastructure builder interface
│   └── investigator.py    # SRE investigator interface
├── README.md              # This documentation
└── tui_main.py            # Main entry point
```

## Features

### 1. Cyberpunk Aesthetic
- Matrix-green, amber-warning, and cyber-red color scheme
- High-contrast, information-dense interface
- Terminal-optimized design
- Glowing borders and status indicators

### 2. Core Functionality
- **Dashboard**: Real-time system metrics and telemetry
- **Forge Builder**: Infrastructure-as-code editor with validation
- **SRE Investigator**: Live log streaming and command injection
- **Global State Management**: Reactive metrics and connection status

### 3. Advanced UI Components
- Sparkline charts for CPU/Memory trends
- Interactive data tables for task monitoring
- Rich log viewer with syntax highlighting
- Tree navigation for infrastructure topology
- Status indicators with visual states (idle, thinking, executing, failed)

### 4. Keyboard-First Navigation
- Hotkey bindings for all major functions
- Command palette access
- Efficient keyboard workflows
- Context-sensitive hints

## How to Run

### Prerequisites
- Python 3.8+
- Textual library (already installed: `pip install textual`)

### Running the Application

1. **Navigate to the project directory:**
   ```bash
   cd C:\Users\Mehtab\Desktop\input\test\Programs\deckforge
   ```

2. **Run the TUI application:**
   ```bash
   python tui_main.py
   ```
   
   OR
   
   ```bash
   python -m tui.app
   ```

### Keyboard Controls
- `Ctrl+Q`: Exit the application
- `Ctrl+D`: Switch to Dashboard
- `Ctrl+F`: Switch to Forge Builder
- `Ctrl+I`: Switch to SRE Investigator
- `Ctrl+P`: Open command palette (when available)
- `F5`: Deploy changes (in Forge Builder)
- `Ctrl+A`: Inject snippet (in Forge Builder)

### Expected Behavior
- The application launches in your terminal
- You'll see a cyberpunk-themed interface with matrix-green text
- Different tabs show different functionality
- Simulated data updates periodically
- The interface responds to keyboard shortcuts

## Architecture

### Thin Client Design
- All heavy computation happens on the backend
- APIBridge handles all communication with DeckForge services
- Circuit-breaker pattern for resilience
- Type-safe communication using Pydantic models

### Reactive State Management
- Global reactive state in the main application
- Automatic UI updates when data changes
- Efficient rendering with Textual's reactive properties
- Real-time metrics updates

### Modular Screen System
- Independent screens for different functions
- Shared state through the main application
- Consistent styling across all components
- Easy to extend with new functionality

## Known Issues

### CSS Parsing Error
The application currently runs without the custom CSS theme due to a Textual internal CSS parsing issue. The core functionality remains intact, but styling defaults to Textual's built-in themes.

To enable custom styling, uncomment the CSS_PATH line in `tui/app.py`:
```python
CSS_PATH = "style.tcss"  # Remove the # to enable custom styling
```

## Development

### Adding New Screens
1. Create a new screen class inheriting from `Screen`
2. Implement the `compose()` method
3. Add reactive properties as needed
4. Register the screen in the main application
5. Add navigation in the header/footer

### Extending Functionality
- Add new API endpoints in `bridge.py`
- Create new data models in `core/schema.py`
- Implement new widgets as needed
- Update the CSS for new components

## Design Philosophy

The DeckForge TUI follows a "SRE Cockpit" metaphor, providing operators with a comprehensive view of their infrastructure while maintaining efficiency through keyboard-driven workflows. The cyberpunk aesthetic reinforces the futuristic, high-tech nature of the platform while maintaining readability and usability.

The interface prioritizes:
- Information density without sacrificing clarity
- Rapid access to critical functions
- Real-time awareness of system state
- Resilient operation in degraded conditions
- Keyboard-first interaction patterns

## Testing

To verify all components work correctly:
```bash
python test_tui_components.py
```

This will test that all modules import correctly and the application can be instantiated.

This implementation transforms the traditional command-line experience into a rich, interactive environment that enhances the capabilities of the underlying DeckForge platform.