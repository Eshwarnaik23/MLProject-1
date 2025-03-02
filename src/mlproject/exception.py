import sys
from src.mlproject.logger import logging

def error_message_detail(error, error_detail: sys):
    exc_type, exc_value, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occurred in script [{file_name}] at line [{exc_tb.tb_lineno}]: {str(error)}"
    return error_message

class CustomException(Exception):
    def __init__(self, error_message: str, error_details: sys):
        exc_type, exc_value, exc_tb = error_details.exc_info()  # Fix
        file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "Unknown"
        line_number = exc_tb.tb_lineno if exc_tb else "Unknown"

        self.error_message = f"Error in script [{file_name}] at line [{line_number}]: {error_message}"
        super().__init__(self.error_message)

    def __str__(self):
        return self.error_message
