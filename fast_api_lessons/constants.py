from enum import Enum

class LoanStatus(str, Enum):
    OVERDUE = "OVERDUE"
    WITHOUT_OVERDUE = "WITHOUT_OVERDUE"
    CLOSED = "CLOSED"

