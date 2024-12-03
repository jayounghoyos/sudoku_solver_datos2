import math
import sys
import copy


def read_sudoku_input():
    """
    Lee un n-Sudoku desde la entrada estándar en formato sin espacios entre celdas.
    Cada celda tiene un tamaño fijo basado en n^2.
    """
    lines = sys.stdin.read().strip().splitlines()
    n = int(lines[0].strip())  # Tamaño de la subcuadrícula
    N = n * n  # Tamaño del Sudoku completo
    num_digits = math.floor(math.log10(N) + 1)  # Dígitos necesarios para representar cada celda

    grid = []
    for line in lines[1:]:
        row = []
        for i in range(0, len(line), num_digits):  # Procesa celdas con tamaño fijo
            cell = line[i:i + num_digits]
            if cell == "-" * num_digits:  # Identifica celdas vacías
                row.append({"value": 0, "notes": set(range(1, N + 1))})
            else:  # Convierte celdas con números
                row.append({"value": int(cell), "notes": set()})
        grid.append(row)
    return n, grid


def update_notes(n, board):
    """
    Actualiza las notas de todas las celdas vacías según las reglas del Sudoku.
    """
    N = n * n
    for r in range(N):
        for c in range(N):
            if board[r][c]["value"] == 0:
                row_values = {board[r][i]["value"] for i in range(N) if board[r][i]["value"] != 0}
                col_values = {board[i][c]["value"] for i in range(N) if board[i][c]["value"] != 0}
                box_values = {
                    board[box_r][box_c]["value"]
                    for box_r in range(r // n * n, r // n * n + n)
                    for box_c in range(c // n * n, c // n * n + n)
                    if board[box_r][box_c]["value"] != 0
                }
                board[r][c]["notes"] = set(range(1, N + 1)) - (row_values | col_values | box_values)
            else:
                board[r][c]["notes"] = set()


def find_hidden_singles(n, board):
    """
    Identifica y asigna solitarios ocultos en filas, columnas y subcuadrículas.
    """
    N = n * n
    updated = False

    # Verificar filas
    for r in range(N):
        candidate_count = {}
        for c in range(N):
            for note in board[r][c]["notes"]:
                candidate_count[note] = candidate_count.get(note, 0) + 1

        for candidate, count in candidate_count.items():
            if count == 1:  # Solitario oculto encontrado
                for c in range(N):
                    if candidate in board[r][c]["notes"]:
                        board[r][c]["value"] = candidate
                        board[r][c]["notes"] = set()
                        updated = True
                        update_notes(n, board)
                        break

    # Verificar columnas
    for c in range(N):
        candidate_count = {}
        for r in range(N):
            for note in board[r][c]["notes"]:
                candidate_count[note] = candidate_count.get(note, 0) + 1

        for candidate, count in candidate_count.items():
            if count == 1:  # Solitario oculto encontrado
                for r in range(N):
                    if candidate in board[r][c]["notes"]:
                        board[r][c]["value"] = candidate
                        board[r][c]["notes"] = set()
                        updated = True
                        update_notes(n, board)
                        break

    # Verificar subcuadrículas
    for box_r in range(0, N, n):
        for box_c in range(0, N, n):
            candidate_count = {}
            for r in range(box_r, box_r + n):
                for c in range(box_c, box_c + n):
                    for note in board[r][c]["notes"]:
                        candidate_count[note] = candidate_count.get(note, 0) + 1

            for candidate, count in candidate_count.items():
                if count == 1:  # Solitario oculto encontrado
                    for r in range(box_r, box_r + n):
                        for c in range(box_c, box_c + n):
                            if candidate in board[r][c]["notes"]:
                                board[r][c]["value"] = candidate
                                board[r][c]["notes"] = set()
                                updated = True
                                update_notes(n, board)
                                break

    return updated


def solve_with_notes_and_backtracking(n, board):
    """
    Resuelve el Sudoku llenando candidatos únicos y usando backtracking.
    """
    N = n * n

    def is_solved():
        return all(board[r][c]["value"] != 0 for r in range(N) for c in range(N))

    def apply_single_candidates():
        """Llena celdas con un único candidato posible."""
        progress = False
        for r in range(N):
            for c in range(N):
                if board[r][c]["value"] == 0 and len(board[r][c]["notes"]) == 1:
                    board[r][c]["value"] = board[r][c]["notes"].pop()
                    progress = True
        return progress

    def backtrack(current_board):
        """Aplica backtracking para resolver el Sudoku."""
        min_notes = float("inf")
        cell_to_try = None

        for r in range(N):
            for c in range(N):
                if current_board[r][c]["value"] == 0 and len(current_board[r][c]["notes"]) < min_notes:
                    min_notes = len(current_board[r][c]["notes"])
                    cell_to_try = (r, c)

        if cell_to_try is None:
            return True

        r, c = cell_to_try
        for candidate in current_board[r][c]["notes"]:
            snapshot = copy.deepcopy(current_board)
            current_board[r][c]["value"] = candidate
            update_notes(n, current_board)
            if solve_with_notes_and_backtracking(n, current_board):
                return True
            current_board = snapshot

        current_board[r][c]["value"] = 0
        return False

    while True:
        update_notes(n, board)
        if is_solved():
            return True
        if not apply_single_candidates() and not find_hidden_singles(n, board):
            break

    return backtrack(board)


if __name__ == "__main__":
    n, grid = read_sudoku_input()
    num_digits = math.floor(math.log10(n * n) + 1)

    if solve_with_notes_and_backtracking(n, grid):
        print(f"{n} Sudoku resuelto:")
        for row in grid:
            print(" ".join(str(cell["value"]).zfill(num_digits) for cell in row))
    else:
        print("No se pudo resolver el Sudoku.")
