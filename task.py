from datetime import datetime
from typing import List


class Bank:
    def __init__(self, name: str, clients=None):
        self.name = name
        self.clients = clients

    def register_client(self, client):
        if self.clients == None:
            self.clients = []
        self.clients.append(client)


class Client:
    def __init__(self, name: str, account_value: float, action_log=None):
        self.name = NameError
        self.account_value = account_value
        if action_log == None:
            self.action_log = []

    def log(self, action) -> str:
        current_time = datetime.now()
        log_message = f"[{current_time}] {action}"
        self.action_log.append(log_message)
        return log_message

    def withdraw(self, amount) -> (int, str):
        withdrawal_condition = amount < self.account_value
        if withdrawal_condition:
            self.account_value -= amount
            msg = self.log(f"Withdrawed {amount}")
            return (self.account_value, msg)

    def deposit(self, amount) -> int:
        deposit_condition = amount > 0
        if deposit_condition:
            self.account_value -= amount
            msg = self.log(f"Deposited {amount}")
            return (self.account_value, msg)
        self.log("Tried to deposit a negative amount.")

    def transfer(self, target_client, amount):
        if amount < self.account_value:
            self.withdraw(amount)
            target_client.deposit(amount)
            msg = f"Client {self.name} transfered {amount} to {target_client.name}"
            self.log(msg)


def main():
    bank = Bank("BigMoneyStacksTrust")
    client = Client("Gunnar Gunnarson", 2137)
    bank.register_client(client)
    logged = client.withdraw(3)
    print(logged)
    client2 = Client("John Johnson", 2137)
    client.transfer(client2, 3)


if __name__ == "__main__":
    main()
