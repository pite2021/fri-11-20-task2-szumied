from dataclasses import dataclass
from typing import List


class Bank:
    def __init__(self, name, clients=[]):
        self.name = name
        self.clients = clients


@dataclass
class Client:
    name: str
    account_value: float
    action_log: List[str]


def main():
    pass


if __name__ == "__main__":
    main()
