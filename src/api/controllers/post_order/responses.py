from fastapi import status
from src.api.exceptions.date_time_passed import DatetimePassedException
from src.api.exceptions.time_is_busy import TimeIsBusyException

post_order_responses = {
    status.HTTP_409_CONFLICT: {
        "description": TimeIsBusyException().detail,
        "content": {
            "application/json": {
                "examples": {
                    **TimeIsBusyException().example,
                    **DatetimePassedException().example,
                },
            },
        },
    },
}
