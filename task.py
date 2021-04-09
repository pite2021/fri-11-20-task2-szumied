from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import List


class Bank:
    def __init__(self, name, clients=None):
        self.name = name
        self.clients = clients

    def register_client(self, client):
        self.clients.append(client)


@dataclass
class Client:
    name: str
    account_value: float
    action_log: List[str] = field(default_factory=lambda: [])

    def log(self, action) -> str:
        current_time = datetime.now().time
        self.action_log.append(f"[{current_time} {action}]")

    def withdraw(self, amount) -> int:
        withdrawal_condition = amount < self.account_value
        if withdrawal_condition:
            self.account_value -= amount
            self.log(f"Withdrawed {amount}")
            return self.account_value

    def deposit(self, amount) -> int:
        deposit_condition = amount > 0
        if withdrawal_condition:
            self.account_value -= amount
            self.log(f"Deposited {amount}")
            return self.account_value
        self.log("Tried to deposit a negative amount.")


def main():
    bank = Bank("BigMoneyStacksTrust")
    client = Client("Gunnar Gunnarson", 2137)


if __name__ == "__main__":
    main()
