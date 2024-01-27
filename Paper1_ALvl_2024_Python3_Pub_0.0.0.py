#Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9.4 programming environment

import random
import os

def Main():
    """
    main()

    Asks for filename and begins the puzzle until user does not input y.

    """
    Again = "y"
    Score = 0
    while Again == "y":
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
        Score = MyPuzzle.AttemptPuzzle()
        print("Puzzle finished. Your score was: " + str(Score))
        Again = input("Do another puzzle? ").lower()

class Puzzle():
    def __init__(self, *args):
        """
        Initializes the puzzle instance, populates puzzle with cells.

        :param args: list
        If user has entered a puzzle name, args is a list containing
        the puzzle file name, the function then fetches the data from this file. If the user has not entered a specific puzzle name,
        a standard puzzle is generated and args is a list with numbers representing grid size and symbols left.

        """
        print(args)
        if len(args) == 1:
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            QPattern = Pattern("Q", "QQ**Q**QQ")
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")

    def __LoadPuzzle(self, Filename):
        """
        Loads the puzzle/populates with info of symbols from the puzzle file. Adds cells unless the symbol is @; if so, it adds a blocked cell to the grid.

        :param Filename: string
                name of puzzle file
        :return:
        """
        try:
            with open(Filename) as f:
                NoOfSymbols = int(f.readline().rstrip())
                for Count in range (1, NoOfSymbols + 1):
                    self.__AllowedSymbols.append(f.readline().rstrip())
                NoOfPatterns = int(f.readline().rstrip())
                for Count in range(1, NoOfPatterns + 1):
                    Items = f.readline().rstrip().split(",")
                    P = Pattern(Items[0], Items[1])
                    self.__AllowedPatterns.append(P)
                self.__GridSize = int(f.readline().rstrip())
                for Count in range (1, self.__GridSize * self.__GridSize + 1):
                    Items = f.readline().rstrip().split(",")
                    if Items[0] == "@":
                        C = BlockedCell()
                        self.__Grid.append(C)
                    else:
                        C = Cell()
                        C.ChangeSymbolInCell(Items[0])
                        for CurrentSymbol in range(1, len(Items)):
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                        self.__Grid.append(C)
                self.__Score = int(f.readline().rstrip())
                self.__SymbolsLeft = int(f.readline().rstrip())
        except:
            print("Puzzle not loaded")

    def SavePuzzle(self):
        with open("puzzle5.txt","w") as save_file:
            save_file.write(f"{len(self.__AllowedSymbols)}\n")
            for symbol in self.__AllowedSymbols:
                save_file.write(f"{symbol}\n")
            save_file.write(f"{len(self.__AllowedPatterns)}\n")
            for pattern in self.__AllowedPatterns:
                save_file.write(f"{pattern.GetPatternSequence()[0]},{pattern.GetPatternSequence()}\n")
            save_file.write(f"{self.__GridSize}\n")
            for cell in self.__Grid:
                if cell.GetSymbol() != "-":
                    save_file.write(f"{cell.GetSymbol()},\n")
                else:
                    save_file.write(",\n")

    def UndoMove(self, Row, Column):




    def AttemptPuzzle(self):
        """
         Displays score before move. Asks user for move (row, column and symbol). Adds symbol then returns the score after calculating
         if there are any new patterns made.
        :return: Score
            Integer representing user's score after each addition of a symbol into the grid.
        """
        Finished = False
        while not Finished:
            self.DisplayPuzzle()
            print("Current score: " + str(self.__Score))
            Row = -1
            Valid = False
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    pass
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass


            Symbol = self.__GetSymbolFromUser()
            self.__SymbolsLeft -= 1
            CurrentCell = self.__GetCell(Row, Column)
            if CurrentCell.CheckSymbolAllowed(Symbol):
                CurrentCell.ChangeSymbolInCell(Symbol)
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)
                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore

            save_question = input("Save game and exit? Y/N")

            if self.__SymbolsLeft == 0:
                Finished = True
            elif save_question.lower() == "y":
                Puzzle.SavePuzzle(self)
                Finished = True
        print()
        self.DisplayPuzzle()
        print()
        return self.__Score

    def __GetCell(self, Row, Column):
        """

        :param Row: int
            row of cell to be fetched
        :param Column: int
            column of cell to be fetched
        :return: Cell
            returns the cell in the specified coordinate.
        :raise: IndexError
            if the coordinates are out of
        """
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()

    def CheckforMatchWithPattern(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = ""
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10
                except:
                    pass
        return 0

    def __GetSymbolFromUser(self):
        """
        asks user for symbol until valid input is entered.
        :return: chr
        """
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ")
        return Symbol

    def __CreateHorizontalLine(self):
        """
        creates a blank line of dashes.
        :return: str
            empty row of dashes
        """
        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line

    def DisplayPuzzle(self):
        """
        Prints the symbols with | before each one. If on the boundary, no symbol after the bar.

        """
        print()
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
        print(self.__CreateHorizontalLine())
        for Count in range(0, len(self.__Grid)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())

class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString

    def MatchesPattern(self, PatternString, SymbolPlaced):
        if SymbolPlaced != self.__Symbol:
            return False
        for Count in range(0, len(self.__PatternSequence)):
            try:
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    return False
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    def GetPatternSequence(self):
      return self.__PatternSequence

class Cell():
    def __init__(self):
        """
        Initialises cell object with empty symbol and list of not allowed symbols.
        """
        self._Symbol = ""
        self.__SymbolsNotAllowed = []

    def GetSymbol(self):
        """
        returns - if cell is empty or symbol if not.

        :return: chr
            returns symbol if not empty
        """
        if self.IsEmpty():
          return "-"
        else:
          return self._Symbol
    
    def IsEmpty(self):
        """
        Checks if symbol is empty
        :return: bool
            True if empty false if no
        """
        if len(self._Symbol) == 0:
            return True
        else:
            return False

    def ChangeSymbolInCell(self, NewSymbol):
        """
        Changes the symbol in a cell with the user inputted one

        :param NewSymbol: chr
            user entered symbol
        """
        self._Symbol = NewSymbol

    def CheckSymbolAllowed(self, SymbolToCheck):
        """
        Checks if symbol is in the not allowed list.

        :param SymbolToCheck: chr
            user inputted symbol.
        :return: True if allowed, false if not.
        """
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False
        return True

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        """
        Adds symbol to the not allowed symbol list

        :param SymbolToAdd: chr
        """
        self.__SymbolsNotAllowed.append(SymbolToAdd)

    def UpdateCell(self):
        pass

class BlockedCell(Cell):
    def __init__(self):
        """
        subclass of Cell. symbol is "@" by default, symbols are always not allowed
        """
        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    def CheckSymbolAllowed(self, SymbolToCheck):
        """

        :param SymbolToCheck: ochr
            user inputted symbol
        :return: False
            always false as the cell is blocked
        """
        return False

if __name__ == "__main__":
    Main()