import os
import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        self.error_details=error_details

        _,_,exc_tb=error_details.exc_info()

        self.lineno=exc_tb.tb_lineno
        self.filename=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occured in python script name [{0}] and line number [{1}] error_message [{2}]".format(self.filename,self.lineno,self.error_message)
    
if __name__=="__main__":

    try:
        logger.logging.info("Enter the try block")
        a=1/0
        print("This will not be printed",a)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
