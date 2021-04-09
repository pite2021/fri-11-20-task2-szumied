from datetime import datetime
from typing import Tuple


class Bank:
    def __init__(self, name: str, clients=None):
        self.name = name
        self.clients = clients

    def register_client(self, client) -> str:
        if self.clients is None:
            self.clients = []
        self.clients.append(client)
        register_log = f"Client {client.name} registered in {self.name}"
        return client.log(register_log)


class Client:
    def __init__(self, name: str, account_value: float, action_log=None):
        self.name = name
        self.account_value = account_value
        if action_log is None:
            self.action_log = []

    def log(self, action) -> str:
        current_time = datetime.now()
        log_message = f"[{current_time}, {self.name}] {action}"
        self.action_log.append(log_message)
        return log_message

    def withdraw(self, amount) -> Tuple[int, str]:
        withdrawal_condition = amount < self.account_value
        if withdrawal_condition:
            self.account_value -= amount
            msg = self.log(f"Withdrew {amount}")
            return (self.account_value, msg)
        fail_msg = "FAILURE: withdrawal exceeded the account value."
        return (self.account_value, self.log(fail_msg))

    def deposit(self, amount) -> Tuple[int, str]:
        deposit_condition = amount > 0
        if deposit_condition:
            self.account_value -= amount
            msg = self.log(f"Deposited {amount}")
            return (self.account_value, msg)
        msg = self.log("FAILURE: Tried to deposit a negative amount.")
        return (self.account_value, msg)

    def transfer(self, target_client, amount) -> Tuple[int, str]:
        if amount < self.account_value:
            self.withdraw(amount)
            target_client.deposit(amount)
            msg = f"Transfered {amount} to {target_client.name}"
            return (self.account_value, self.log(msg))

        fail_msg = "Transfered amount exceededing acount value"
        return (self.account_value, self.log(fail_msg))


def main():
    bank = Bank("BigMoneyStacksTrust")
    client = Client("Gunnar Gunnarson", 2137)
    msg = bank.register_client(client)
    print(msg)
    msg = client.withdraw(3)
    print(msg)
    client2 = Client("John Johnson", 2137)
    msg = client.transfer(client2, 3)
    print(msg)


if __name__ == "__main__":
    main()
