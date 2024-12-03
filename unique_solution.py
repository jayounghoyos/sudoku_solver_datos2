import random
import sys

class SudokuGenerator:
    def __init__(self, box_size):
        # Tamaño de la caja (número de filas y columnas por subcuadrícula)
        self.box_size = box_size
        # El tamaño total del tablero (n x n)
        self.n = box_size * box_size
        # Generar el Sudoku completo (sin celdas vacías al principio)
        self.grid = self.generate_sudoku()
    
    def generate_sudoku(self):
        # Generar una cuadrícula base completa
        grid = self.generate_base_grid()
        # Mezclar la cuadrícula aplicando transformaciones aleatorias
        grid = self.shuffle_grid(grid)
        # Eliminar números para crear el rompecabezas (dejar aproximadamente el 75% de las celdas llenas)
        clues = self.n * self.n * 3 // 4
        grid = self.remove_numbers(grid, clues)
        return grid

    def generate_base_grid(self):
        # Generar la cuadrícula base con los números dispuestos en secuencia para un Sudoku completo
        grid = [[((i * self.box_size + i // self.box_size + j) % self.n) + 1 for j in range(self.n)] for i in range(self.n)]
        return grid

    def shuffle_grid(self, grid):
        # Intercambiar filas, columnas, bandas y pilas para mezclar el Sudoku
        n = self.n
        box_size = self.box_size

        # Función para intercambiar filas
        def swap_rows(grid, row1, row2):
            grid[row1], grid[row2] = grid[row2], grid[row1]

        # Función para intercambiar columnas
        def swap_columns(grid, col1, col2):
            for row in grid:
                row[col1], row[col2] = row[col2], row[col1]

        # Intercambiar filas dentro de cada banda (conjunto de filas contiguas)
        for band in range(box_size):
            rows = [band * box_size + i for i in range(box_size)]
            random.shuffle(rows)  # Mezclar las filas de esta banda
            for i in range(box_size):
                swap_rows(grid, band * box_size + i, rows[i])

        # Intercambiar columnas dentro de cada pila (conjunto de columnas contiguas)
        for stack in range(box_size):
            cols = [stack * box_size + i for i in range(box_size)]
            random.shuffle(cols)  # Mezclar las columnas de esta pila
            for i in range(box_size):
                swap_columns(grid, stack * box_size + i, cols[i])

        # Intercambiar bandas completas (grupos de filas)
        bands = list(range(box_size))
        random.shuffle(bands)
        temp_grid = grid[:]
        for i in range(box_size):
            for j in range(box_size):
                grid[i * box_size + j] = temp_grid[bands[i] * box_size + j]

        # Intercambiar pilas completas (grupos de columnas)
        stacks = list(range(box_size))
        random.shuffle(stacks)
        temp_grid = [row[:] for row in grid]
        for i in range(n):
            for j in range(box_size):
                for k in range(box_size):
                    grid[i][j * box_size + k] = temp_grid[i][stacks[j] * box_size + k]

        # Intercambiar números en la cuadrícula (para cambiar su orden)
        numbers = list(range(1, n + 1))
        shuffled_numbers = numbers[:]
        random.shuffle(shuffled_numbers)
        mapping = {numbers[i]: shuffled_numbers[i] for i in range(n)}
        for i in range(n):
            for j in range(n):
                grid[i][j] = mapping[grid[i][j]]

        return grid

    def remove_numbers(self, grid, clues):
        # Eliminar números al azar hasta que queden solo las pistas necesarias
        n = self.n
        total_cells = n * n
        cells_to_remove = total_cells - clues
        while cells_to_remove > 0:
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)

            if grid[i][j] != 0:
                # Eliminar el número en la celda y su celda simétrica (para mantener el equilibrio)
                grid[i][j] = 0
                grid[n - 1 - i][n - 1 - j] = 0
                cells_to_remove -= 2

        return grid

    def print_grid(self, digits):
        # Imprimir la cuadrícula con el formato adecuado
        for i in range(self.n):
            row = []
            for j in range(self.n):
                if self.grid[i][j] == 0:
                    row.append('-' * digits)  # Celdas vacías representadas con guiones
                else:
                    row.append(self._symbol(self.grid[i][j], digits))
            print(''.join(row))

    def _symbol(self, num, digits):
        # Representar un número con un mínimo de 'digits' dígitos (rellenar con ceros si es necesario)
        return str(num).zfill(digits)
    
def main():
    sudoku_counts = {}

    #leer lineas de entrada
    lines = sys.stdin.read().splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            #leer el tamaño de la caja del sudoku
            box_size = int(line)
        except ValueError:
            continue    #ignorar entradas que no sean números válidos

        #calcular el tamaño total del tablero
        n = box_size * box_size

        # Inicializar el contador si es necesario
        if n not in sudoku_counts:
            sudoku_counts[n] = 0
        sudoku_number = sudoku_counts[n]
        sudoku_counts[n] += 1

        # Generar el Sudoku
        sudoku = SudokuGenerator(box_size)

        # Imprimir el encabezado del Sudoku
        print(f"{box_size}-Sudoku #{sudoku_number}")
        print()

        # Calcular el número de dígitos por número en el tablero
        digits = len(str(sudoku.n))

        # Imprimir la cuadrícula del Sudoku
        sudoku.print_grid(digits)

        # Imprimir una línea en blanco entre Sudokus
        print()
    

if __name__ == "__main__":
    main()
