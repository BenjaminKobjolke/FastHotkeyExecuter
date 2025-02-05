class InternalCommandManager:
    def __init__(self):
        self.commands = [
            {
                "name": "exit - quit",
                "command": "exit"
            }
        ]

    def search_commands(self, search_text: str) -> list:
        """Search through available commands."""
        if not search_text:
            return self.commands
            
        search_text = search_text.lower()
        return [
            cmd for cmd in self.commands 
            if search_text in cmd["name"].lower()
        ]

    def execute_command(self, command: dict) -> None:
        """Execute the selected command."""
        if command["command"] == "exit":
            return "exit"
        return None
