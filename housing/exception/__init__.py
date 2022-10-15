import os
import sys

class HousingException(Exception):
    ## sys module will contain details of error like on which line of which file error occured etc
    def __init__(self, error_message:Exception,error_detail:sys):

        ## Here we are passing the error message i.e. exception occured to the parent class i.e Exception class as we have inherited 
        ## Exception class
        super().__init__(error_message)
        self.error_message=HousingException.get_detailed_error_message(error_message=error_message,error_detail=error_detail)

    ## We are trying to define method that will return detailed error message in form of string
    ## static method can be called without object creation
    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_detail:sys)->str:
        _,_,exec_tb=error_detail.exc_info()

        ## error Line number
        line_number=exec_tb.f_lineno

        ## error file name
        file_name=exec_tb.tb_frame.f_code.co_filename

        ## Prepare error message
        error_message=f'Error occured in file [{file_name}] at line number [{line_number}] and error message is [{error_message}]'
        return error_message

    def __str__(self) :
        return self.error_message

    def __repr__(self):
        return HousingException.__name__.str()
        