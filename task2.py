from datetime import datetime
from typing import Tuple
from typing import List
import functools
import logging

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)


class Bank:
    def __init__(self, name: str, clients: List[str] = None):
        self.name = name
        self.clients = clients

    def register_client(self, client) -> str:
        if self.clients is None:
            self.clients = []
        self.clients.append(client)
        register_log = f"Client {client.name} registered in {self.name}"
        return client.log(register_log)

    def total_acounts_value(self) -> float:
        account_values = [client.account_value for client in self.clients]
        result = functools.reduce(lambda acc, next: acc + next, account_values)
        return result


class BankActionError(Exception):
    pass


class Client:
    def __init__(self, name: str, account_value: float, action_log=None):
        self.name = name
        self.account_value = account_value
        if action_log is None:
            self.action_log = []

    def protected_account_action(self, condition, failure_msg, success_msg, action, action_params=None):
        try:
            if condition:
                action(action_params)
                msg = self.log(success_msg)
                return (self.account_value, msg)
            raise BankActionError("(EXCEPTION) {}".format(failure_msg))
        except BankActionError as ex:
            msg = self.log("{}".format(str(ex)))
            return (self.account_value, msg)

    def withdraw(self, amount: float) -> Tuple[int, str]:
        withdrawal_condition = amount < self.account_value
        fail_msg = "FAILURE: withdrawal exceeded the account value"
        success_msg = "SUCCEESS: withdrew {}".format(amount)
        action = lambda account: (
            setattr(account, "account_value", account.account_value - amount)
        )
        result = self.protected_account_action(
            withdrawal_condition, fail_msg, success_msg, action, action_params=self
        )
        return result

    def deposit(self, amount: float) -> Tuple[int, str]:
        deposit_condition = amount > 0
        fail_msg = "FAILURE: deposit value too low."
        success_msg = "SUCCEESS: Deposited {}".format(amount)
        action = lambda account: (
            setattr(account, "account_value", account.account_value + amount)
        )
        result = self.protected_account_action(
            deposit_condition, fail_msg, success_msg, action, action_params=self
        )
        return result

    def log(self, action: str) -> str:
        current_time = datetime.now()
        log_message = f"[{current_time}, {self.name}] {action}. (Account value: {self.account_value})"
        self.action_log.append(log_message)
        return log_message

    def transfer(self, target_client, amount: float) -> Tuple[int, str]:
        transfer_condition = amount < self.account_value
        fail_msg = "FAILURE: Transfered amount exceededing account value"
        success_msg = "SUCCEESS: Transfered {} to {}".format(amount, target_client.name)

        def action_body(params):
            params["self"].withdraw(params["amount"])
            params["target"].deposit(params["amount"])
        params = {"self": self, "target": target_client, "amount": amount}
        result = self.protected_account_action(
            transfer_condition, fail_msg, success_msg, action_body, action_params=params
        )
        return result


def main():
    bank = Bank("BigMoneyStacksTrust")
    client = Client("Gunnar Gunnarson", 2137)
    bank.register_client(client)
    client.withdraw(3)
    client2 = Client("John Johnson", 2132)
    bank.register_client(client2)
    client.transfer(client2, 3)
    client.withdraw(233333)
    client.transfer(client2, 324134134)
    [logging.info(action) for action in client.action_log]
    total = bank.total_acounts_value()
    logging.info("Summed accounts' value: {}".format(total))


if __name__ == "__main__":
    main()
