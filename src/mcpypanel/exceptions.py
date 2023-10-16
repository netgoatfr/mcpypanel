
class WizardError(Exception):pass
class AccountManagerError(WizardError):pass
class AccountNotFoundError(AccountManagerError):pass
class AccountAlreadyExist(AccountManagerError):pass