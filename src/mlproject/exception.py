import sys
from src.mlproject.logger import logging
import logging

def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message


class CustomException(Exception):
    def __init__(self, error_message: str, error_details):
        exc_type, exc_value, exc_tb = error_details  
        file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown"
        line_number = exc_tb.tb_lineno if exc_tb else "Unknown"

        # Properly format error message
        self.error_message = f"Error in script [{file_name}] at line [{line_number}]: {error_message}"
        super().__init__(self.error_message)

    def __str__(self):
        return self.error_message

