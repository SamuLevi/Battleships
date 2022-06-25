from ship import Ship
import random

# Variablen die für den jeweiligen Status des Schiffs stehen
EMPTY = 0
SHIP = 1
HIT = 2
MISS = 3


# Klasse initialisiert Spielfeld und Methoden darin machen alles, was damit zusammenhängt
class Board:
    # Initialisierung Spielfeld
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        # Alle Schiffe auf dem Spielfeld werden in folgender Liste gespeichert
        self.ships = []

        # Erstellt 2D Liste für das Spielfeld, 0 bedeutet hier, dass es vorerst leer ist
        self.board = [([EMPTY] * cols) for _ in range(rows)]

    # Platziert neues Schiff auf dem Spielfeld
    def addShip(self, ship: Ship):
        # Ist die Koordinate schon von einem Schiff besetzt? Wenn ja, gib False aus (Schiff wird nicht platziert)
        for i in range(ship.size):
            if self.board[ship.coordinates[i][0]][ship.coordinates[i][1]] == SHIP:
                return False

        # Ist die Koordinate außerhalb des Spielfeldes? Wenn ja, gib False aus (Schiff wird nicht platziert)
        for j in range(ship.size):
            if not 0 <= self.board[ship.coordinates[j][0]][ship.coordinates[j][1]] < self.rows:
                return False

        # Setzt alle Felder des Schiffs auf besetzt (Platziert Schiff)
        for i in range(ship.size):
            self.board[ship.coordinates[i][0]][ship.coordinates[i][1]] = SHIP

        # Setzt Schiff auf Liste aller Schiffe
        self.ships.append(ship)

        # Gib True aus, wenn alles platziert wurde und geklappt hat.
        return True


    # Attackiert beliebige Koordinate
    def bomb(self, row, col):
        status = self.board[row][col]
        if status == EMPTY:
            # Vorbei am Schiff
            self.board[row][col] = MISS
            result = f"({row + 1},{col + 1}) -> Miss"
        elif status == SHIP:
            # Schiff getroffen
            self.board[row][col] = HIT

            # Getroffenes Schiff ausfindig machen
            bombedShip = ()
            for ship in self.ships:
                for i in ship.coordinates:
                    if i == (row, col):
                        bombedShip = ship

            # Überprüfung, ob Schiff bereits zerstört wurde
            if self.isShipDestroyed(bombedShip):
                # Falls ja, wird das Schiff von der Liste entfernt
                self.ships.remove(bombedShip)
                # Ob alle Schiffe zerstört sind, ein Schiff zerstört wurde oder ein einfacher Treffer gelandet wurde
                # Nachricht ausgeben
                if self.isGameOver():
                    result = f"({row + 1},{col + 1}) -> Destroyed, game over"
                else:
                    result = f"({row + 1},{col + 1}) -> Destroyed"
            else:
                result = f"({row + 1},{col + 1}) -> Hit"
        # Falls Koordinate bereits angegriffen wurde
        else:
            result = f"({row + 1},{col + 1}) -> Bombed already"

        print(result)

        return result

    # Methode, die überprüft, ob Schiff zerstört ist
    def isShipDestroyed(self, ship: Ship):
        for i in range(ship.size):
            if self.board[ship.coordinates[i][0]][ship.coordinates[i][1]] == SHIP:
                return False
        return True

    # Methode, die überprüft ob es noch Schiffe gibt
    def isGameOver(self):
        # Gibt True aus, wenn Liste der Schiffe leer aus, ansonsten False
        return not self.ships

    # Zeigt Spielfeld an
    def display(self):
        print(self.info())

    # Generiert Spielfeld-Infos
    def info(self):
        row_index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        info ="  " + " ".join(str(i) for i in range(1, self.cols + 1))
        for r in range(self.rows):
            row = row_index[r] + " "
            for c in range(self.cols):
                if self.board[r][c] == HIT:
                    row += ' '
                elif self.board[r][c] == MISS:
                    row += 'o '
                else:
                    row += '- '
            info = info + "\n" + row + "  "
        return info

    # Zeigt Koordinaten an mit allem (für Platzierung, nicht verdeckt)
    def displayDebug(self):
        row_index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        print("  " + " ".join(str(i) for i in range(1, self.cols + 1)))
        for i in range(self.rows):
            line = row_index[i] + " "
            for j in range(self.cols):
                line += str(self.board[i][j])
                line += " "
            print(line)
