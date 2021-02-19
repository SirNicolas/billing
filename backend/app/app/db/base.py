# Import all the models, so that Base has them before being
from app.db.base_class import Base  # noqa
from app.common.wallet.model import Wallet, Transaction  # noqa
from app.common.user.model import User  # noqa
