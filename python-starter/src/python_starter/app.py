"""Core application behavior."""


def make_greeting(name: str) -> str:
    """Return a friendly greeting for a non-empty name."""
    cleaned_name = name.strip()
    if not cleaned_name:
        raise ValueError("name must not be empty")
    return f"Hello, {cleaned_name}!"


def main() -> None:
    """Run the command-line application."""
    print(make_greeting("Developer"))
