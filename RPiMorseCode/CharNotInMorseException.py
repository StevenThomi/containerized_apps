##
# Custom Exception Class: CharNotInMorseException
# Inherits from: SyntaxError
# Author: Steve Thomi
# Licence: MIT
# Description: Supports case char keyed in is not in a-z, 0-9

class CharNotInMorseException(SyntaxError):
    ## The constructor
    # @param self the object pointer
    # @param char the invalid symbol (i.e., %,*)
    def __init__(self, char):
        super().__init__()
        self.setChar(char)

    ## The mutator
    # @param self the object pointer
    # @param char the invalid symbol (i.e., %,*)
    def setChar(self, char):
        self.__char = char

    ## The accessor
    # @param self the object pointer
    # return character
    def getChar(self):
        return self.__char
