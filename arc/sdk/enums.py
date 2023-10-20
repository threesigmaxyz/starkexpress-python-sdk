from enum import Enum


class Environment(Enum):
    TESTNET = 0
    MAINNET = 1


class TransactionType(Enum):
    Deposit = "Deposit"
    Transfer = "Transfer"
    Mint = "Mint"
    Withdrawal = "Withdrawal"


class AssetType(Enum):
    ETH = 0
    ERC20 = 1
    ERC721 = 2
    ERC1155 = 3
    ERC20_MINTABLE = 4
    ERC721_MINTABLE = 5
    ERC1155_MINTABLE = 6


class DataAvailabilityMode(Enum):
    VALIDIUM = 0
    ZK_ROLLUP = 1
