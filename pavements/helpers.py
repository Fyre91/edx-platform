import os


class cd:
    """
    Wrap change directory

    From http://stackoverflow.com/questions/431684/how-do-i-cd-in-python
    """

    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
