from fastapi import status
from src.utils.http_docs_exception import HTTPDocsException


class DatetimePassedException(HTTPDocsException):
    """Exception for when the selected time and date have already passed."""

    def __init__(self):
        """Initialize the exception."""
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Selected time and date have already passed.",
        )
