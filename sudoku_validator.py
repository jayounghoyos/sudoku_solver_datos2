import sys
import math

class SudokuValidator:
    def __init__(self, grid):
        """Inicializa el validador de Sudoku con la cuadrícula dada."""
        self.grid = grid
        self.n = len(grid)  # Tamaño de la cuadrícula (n x n)
        self.box_size = int(math.sqrt(self.n))  # Tamaño de la subcuadrícula (raíz cuadrada de n)
        # Validar que n sea un cuadrado perfecto
        if self.box_size ** 2 != self.n:
            raise ValueError("El tamaño de la cuadrícula no es válido. n debe ser un cuadrado perfecto.")
        # Números permitidos en el Sudoku
        self.numbers = set(range(1, self.n + 1))

    def is_valid(self):
        """Verifica si el Sudoku es válido en filas, columnas y subcuadrículas."""
        return self._check_rows() and self._check_columns() and self._check_boxes()

    def _check_rows(self):
        """Verifica que no haya duplicados en las filas."""
        for i in range(self.n):
            row = [num for num in self.grid[i] if num != 0]
            if len(row) != len(set(row)):  # Duplicado encontrado
                print(f"Error en la fila {i + 1}")
                return False
        return True

    def _check_columns(self):
        """Verifica que no haya duplicados en las columnas."""
        for j in range(self.n):
            column = [self.grid[i][j] for i in range(self.n) if self.grid[i][j] != 0]
            if len(column) != len(set(column)):  # Duplicado encontrado
                print(f"Error en la columna {j + 1}")
                return False
        return True

    def _check_boxes(self):
        """Verifica que no haya duplicados en las subcuadrículas."""
        for box_row in range(0, self.n, self.box_size):
            for box_col in range(0, self.n, self.box_size):
                box = []
                for i in range(box_row, box_row + self.box_size):
                    for j in range(box_col, box_col + self.box_size):
                        if self.grid[i][j] != 0:
                            box.append(self.grid[i][j])
                if len(box) != len(set(box)):  # Duplicado encontrado en una subcuadrícula
                    print(f"Error en la caja que comienza en ({box_row + 1},{box_col + 1})")
                    return False
        return True
    
def main():
    input_lines = sys.stdin.read().splitlines()  # Leer la entrada completa
    idx = 0

    while idx < len(input_lines):
        n_line = input_lines[idx].strip()
        idx += 1
        if not n_line:
            continue

        # Leer el tamaño de la subcuadrícula (n)
        n = int(n_line[0])

        # Saltar líneas vacías
        while idx < len(input_lines) and input_lines[idx].strip() == '':
            idx += 1

        N = n * n  # El tamaño del Sudoku completo (n x n)
        sudoku = []

        # Leer la cuadrícula del Sudoku
        for _ in range(N):
            if idx >= len(input_lines):
                break
            s = input_lines[idx].strip()
            idx += 1
            while not s and idx < len(input_lines):
                s = input_lines[idx].strip()
                idx += 1

            if not s:
                break

            # Determinar el número de dígitos por símbolo
            line_length = len(s)
            num_symbols = N
            num_digits_per_symbol = line_length // num_symbols
            if num_digits_per_symbol == 0:
                num_digits_per_symbol = 1  # Asignar un valor por defecto si es 0

            # Dividir la línea en símbolos del tamaño adecuado
            row_symbols = [s[i:i+num_digits_per_symbol] for i in range(0, len(s), num_digits_per_symbol)]

            # Convertir los símbolos en enteros, tratando las celdas vacías
            row_int = []
            for symbol in row_symbols:
                symbol = symbol.strip()
                if symbol == '-' * num_digits_per_symbol or symbol == '':
                    num = 0  # Representa una celda vacía
                else:
                    num = int(symbol)
                row_int.append(num)
            sudoku.append(row_int)

        # Validar el Sudoku
        try:
            validator = SudokuValidator(sudoku)
            if validator.is_valid():
                print("El sudoku es válido")
            else:
                print("El sudoku no es válido")
        except ValueError as e:
            print(f"Error: {e}")

        # Línea en blanco entre Sudokus
        print()

if __name__ == "__main__":
    main()