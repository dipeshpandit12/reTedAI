from dataclasses import dataclass


@dataclass(frozen=True)
class AllowedAction:
    name: str
    command: tuple[str, ...]
    description: str


ACTIONS = {
    "check_processes": AllowedAction("check_processes", ("ps", "aux"), "List running processes."),
    "disk_usage": AllowedAction("disk_usage", ("df", "-h"), "Report filesystem usage."),
}
