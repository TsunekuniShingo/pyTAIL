import time
import traceback

from contextlib import contextmanager



class Timer:
    def __new__(cls):
        if not hasattr(cls, "__instance__"):
            cls.__instance__ = super().__new__(cls)

        cls.__instance__._count = 0
        cls.__instance__._RECORD = {}
        cls.__instance__._RECORDDESCRIPTION = {}
        return cls.__instance__


    def __init__(self):
        pass


    @contextmanager
    def timer(self,message=None):
        if __debug__:
            self._count += 1
            t = time.time()
            if message:
                if not isinstance(message,str):
                    message = f'{StdOutColour.reverse}'\
                              f'Argument is not str so the message is ignored'\
                              f'{StdOutColour.E}'
                self._RECORDDESCRIPTION[self._count] = message
            try:
                yield
                elapsedTime = time.time()-t
                self._RECORD[self._count] = elapsedTime
            except:
                print(traceback.format_exc())
                self.show()
                raise Exception(traceback.format_exc())
        else:
            yield

    def show(self):
        if __debug__:
            for key,val in self._RECORD.items():
                print(f'No.{key} block takes '\
                      f'{StdOutColour.red}{val}{StdOutColour.E}[s]'
                )
                if key in self._RECORDDESCRIPTION:
                    print("---- DESCRIPTION : {}\n".format(self._RECORDDESCRIPTION[key]))
                else:
                    print("\n")
        else:
            pass



class StdOutColour:
    black = '\033[30m'
    b_black = '\033[40m'
    red = '\033[31m'
    b_red = '\033[41m'
    green = '\033[32m'
    b_green = '\033[42m'
    yellow = '\033[33m'
    b_yellow = '\033[43m'
    blue = '\033[34m'
    b_blue = '\033[44m'
    purple = '\033[35m'
    b_purple = '\033[45m'
    cyan = '\033[36m'
    b_cyan = '\033[46m'
    white = '\033[37m'
    b_white = '\033[47m'
    reverse = '\033[07m' 
    accent = '\033[01m'

    E = '\033[0m'