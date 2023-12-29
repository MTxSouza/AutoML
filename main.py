"""
Base script to initialize the AutoML application.
"""
import os


def build_logging_folder() -> None:
    """
    Initializes the folder to store
    all log files.
    """
    folder_name = "logs"
    if not os.path.exists(path=folder_name):
        os.mkdir(path=folder_name)


if __name__=="__main__":
    
    # initialize folders
    build_logging_folder()
