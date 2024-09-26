from enum import Enum


class ModeEnum(str, Enum):
    """Enum for app mode."""

    PROD = "PROD"
    TEST = "TEST"
