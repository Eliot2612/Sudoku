import random
import time
import os

SIZE = 9
BOX = 3

def is_safe(grid, row, col, num):
    """Check if num can be placed at (row, col) without breaking Sudoku rules."""
    # Row
    if num in grid[row]:
        return False
    # Column
    if any(grid[i][col] == num for i in range(SIZE)):
        return False
    # 3x3 Box
    box_row, box_col = (row // BOX) * BOX, (col // BOX) * BOX
    for i in range(BOX):
        for j in range(BOX):
            if grid[box_row + i][box_col + j] == num:
                return False
    return True

def fill_box(grid, row, col):
    """Fill a 3x3 box starting at (row, col) with numbers randomly."""
    nums = random.sample(range(1, SIZE+1), SIZE)
    idx = 0
    for i in range(BOX):
        for j in range(BOX):
            grid[row + i][col + j] = nums[idx]
            idx += 1

def fill_diagonal(grid):
    """Fill the three diagonal boxes to simplify solving."""
    for i in range(0, SIZE, BOX):
        fill_box(grid, i, i)

def fill_remaining(grid, row=0, col=0):
    """Recursively fill remaining cells with valid numbers."""
    if col >= SIZE:
        row += 1
        col = 0
    if row >= SIZE:
        return True  # completed

    # Skip cells in diagonal boxes
    if row < BOX:
        if col < BOX:
            col = BOX
    elif row < SIZE - BOX:
        if col == (row // BOX) * BOX:
            col += BOX
    else:
        if col == SIZE - BOX:
            row += 1
            col = 0
            if row >= SIZE:
                return True

    for num in random.sample(range(1, SIZE+1), SIZE):
        if is_safe(grid, row, col, num):
            grid[row][col] = num
            if fill_remaining(grid, row, col + 1):
                return True
            grid[row][col] = 0  # backtrack

    return False

def count_solutions(grid):
    """Count number of solutions for a Sudoku grid (stop at >1)."""
    count = [0]

    def solve():
        for i in range(SIZE):
            for j in range(SIZE):
                if grid[i][j] == 0:
                    for num in range(1, SIZE+1):
                        if is_safe(grid, i, j, num):
                            grid[i][j] = num
                            solve()
                            grid[i][j] = 0
                    return
        count[0] += 1
        if count[0] > 1:
            return

    solve()
    return count[0]

def remove_k_digits_unique(grid, k):
    """Remove k numbers randomly, ensuring puzzle still has a unique solution."""
    attempts = k
    while attempts > 0:
        i, j = random.randint(0, SIZE-1), random.randint(0, SIZE-1)
        if grid[i][j] == 0:
            continue
        backup = grid[i][j]
        grid[i][j] = 0

        # Make a copy for solving
        temp = [row[:] for row in grid]

        if count_solutions(temp) != 1:
            grid[i][j] = backup  # restore if not unique
        else:
            attempts -= 1

def generate_unique_sudoku(k):
    """Generate a Sudoku puzzle with k empty cells and unique solution."""
    grid = [[0]*SIZE for _ in range(SIZE)]
    fill_diagonal(grid)
    fill_remaining(grid)
    remove_k_digits_unique(grid, k)
    return grid

def print_grid(grid):
    for r in range(SIZE):
        if r % BOX == 0 and r != 0:
            print("-" * 21)
        for c in range(SIZE):
            if c % BOX == 0 and c != 0:
                print("|", end=" ")
            print(grid[r][c] if grid[r][c] != 0 else ".", end=" ")
        print()

def print_grid_visual(grid):
    """Print the grid to console with a short delay for visual effect."""
    os.system('cls' if os.name == 'nt' else 'clear')  # clear console
    for r in range(SIZE):
        if r % BOX == 0 and r != 0:
            print("-" * 21)
        for c in range(SIZE):
            if c % BOX == 0 and c != 0:
                print("|", end=" ")
            print(grid[r][c] if grid[r][c] != 0 else ".", end=" ")
        print()
    time.sleep(0.05)  # speed of visualization

def solve_visual(grid):
    """Solve the Sudoku grid with step-by-step visual output."""
    for i in range(SIZE):
        for j in range(SIZE):
            if grid[i][j] == 0:
                for num in range(1, SIZE+1):
                    if is_safe(grid, i, j, num):
                        grid[i][j] = num
                        print_grid_visual(grid)
                        if solve_visual(grid):
                            return True
                        grid[i][j] = 0  # backtrack
                        print_grid_visual(grid)
                return False
    return True

if __name__ == "__main__":
    sudoku = generate_unique_sudoku(25)
    print("Generated Sudoku Puzzle:")
    print_grid(sudoku)

    input("\nPress Enter to watch the Sudoku being solved visually...")

    solve_visual(sudoku)
    print("\nSolved Sudoku:")
    print_grid(sudoku)
