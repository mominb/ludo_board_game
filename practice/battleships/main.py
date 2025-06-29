import random

from grids import Grid


def main():
    grid = make_grid()
    ship_one = hide_ship()
    ship_two = ship_one
    ship_three = hide_ship()

    while ship_one == ship_two or ship_two == ship_three or ship_three == ship_one:
        ship_one = hide_ship()
        ship_two = hide_ship()
        ship_three = hide_ship()

    remaining = 3
    tries = 10
    while remaining != 0 and tries != 0:
        print(grid)
        attack_pos = get_attack()
        grid, success = confirm_damage(grid, attack_pos, ship_one, ship_two, ship_three)
        if success:
            remaining -= 1
        tries -= 1
    if remaining == 0:
        ...
    elif tries == 0:
        ...


def make_grid():
    x = [2, 3, 4, 5, 6]
    y = [2, 3, 4, 5, 6]
    grid = Grid(6, 6)
    grid.update_cell(1, 1, 0)
    grid.update_cell(1, 2, 1)
    grid.update_cell(1, 3, 2)
    grid.update_cell(1, 4, 3)
    grid.update_cell(1, 5, 4)
    grid.update_cell(1, 6, 5)
    grid.update_cell(1, 1, 0)
    grid.update_cell(2, 1, 1)
    grid.update_cell(3, 1, 2)
    grid.update_cell(4, 1, 3)
    grid.update_cell(5, 1, 4)
    grid.update_cell(6, 1, 5)

    for numy in y:
        for numx in x:
            grid.update_cell(numx, numy, ".")

    return grid


def get_attack():
    print("Enter target position")
    x = int(input("X-coordinates?  ")) + 1
    y = int(input("Y-coordinates?  ")) + 1

    return x, y


def hide_ship():
    x = random.randint(2, 6)
    y = random.randint(2, 6)

    return (x, y)


def confirm_damage(grid, attack_pos, ship_one, ship_two, ship_three):
    success = True
    if attack_pos == ship_one:
        (x, y) = ship_one
        grid.update_cell(x, y, "X")

    elif attack_pos == ship_two:
        (x, y) = ship_two
        grid.update_cell(x, y, "X")
    elif attack_pos == ship_three:
        (x, y) = ship_three
        grid.update_cell(x, y, "X")
    else:
        (x, y) = attack_pos
        grid.update_cell(x, y, "O")
        success = False

    return grid, success


if __name__ == "__main__":
    main()
