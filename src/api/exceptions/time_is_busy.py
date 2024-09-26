from fastapi import status
from src.utils.http_docs_exception import HTTPDocsException


class TimeIsBusyException(HTTPDocsException):
    """Exception for when the selected date and time is busy."""

    def __init__(self):
        """Initialize the exception."""
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Selected date and time is busy.",
        )
