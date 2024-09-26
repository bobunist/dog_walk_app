from abc import ABC

from fastapi import HTTPException


class HTTPDocsException(HTTPException, ABC):
    """HTTPException with a detail that can be used for documentation."""

    def __init__(
        self,
        status_code: int,
        detail: str,
    ):
        """
        Initialize the HTTPDocsException.

        Args:
            status_code (int): The HTTP status code.
            detail (str): The detail message.

        """
        super().__init__(
            status_code=status_code,
            detail=detail,
        )

    @property
    def example(self) -> dict:
        """
        Get the example response for the exception.

        Returns:
            dict: The example response.

        """
        return {
            self.detail: {
                "value": {
                    "detail": self.detail,
                },
            },
        }
