NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, -1)
WEST = (0, 1)

ANTI_DIRECTION = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}
PRINT_DIRECTION = {
    NORTH: "↑",
    SOUTH: "↓",
    EAST: "←",
    WEST: "→",
}
DIRECTION = {
    "|": {NORTH: SOUTH, SOUTH: NORTH},
    "-": {EAST: WEST, WEST: EAST},
    "L": {NORTH: WEST, WEST: NORTH},
    "J": {NORTH: EAST, EAST: NORTH},
    "7": {SOUTH: EAST, EAST: SOUTH},
    "F": {WEST: SOUTH, SOUTH: WEST},
    ".": {}
}


def print_grid(maze: list) -> None:
    """
    Print a maze as a grid
    :param maze: maze
    :return: None
    """
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            print(maze[i][j], end="")
        print()


def find_start_position(maze: list):
    """
    Find the starting position
    :param maze: maze
    :return: coordinates of the start position
    """
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == "S":
                return i, j


def find_path(maze: list[str]):
    """
    Based on the condition, in my solution I expect a correct maze in which the starting position is part of the ring.
    Additional checks can be added for reliability.
    :param maze:
    :return int: number of steps to the point furthest from the starting position
            list: track with start position and ring
    """

    start = find_start_position(maze)

    queue: list[tuple[tuple, tuple, int]] = []  # (coordinates, exit direction, distances)
    # Look at the neighboring cells and if there is an entrance to the pipe on the side where the Start is,
    # then it is one of the entrances to the loop.
    for di, dj in [WEST, EAST, SOUTH, NORTH]:
        ni, nj = start[0] + di, start[1] + dj
        if (
                0 <= ni < len(maze) and 0 <= nj < len(maze[0])
                and ANTI_DIRECTION[di, dj] in DIRECTION[maze[ni][nj]]
        ):
            queue.append(((ni, nj), (di, dj), 1))
    assert len(queue) == 2
    # create maze for visualization path and distances
    track_maze = [["." for _ in range(len(maze[0]))] for _ in range(len(maze))]
    track_maze[start[0]][start[1]] = "s"

    # Then we go around both ends of the pipe until they meet.
    previous_point: tuple[int, int] = (start[0], start[1])
    while True:
        (i, j), (exit_i, exit_j), distance = queue.pop(0)
        # print_grid(track_maze)
        # print(distance)

        # To determine where the pipe goes, you need to know what its shape is and where it has an inlet.
        shape: str = maze[i][j]
        # The exit direction of the previous pipe is the opposite direction to the inlet
        direction: tuple[int, int] = ANTI_DIRECTION[exit_i, exit_j]
        di, dj = DIRECTION[shape][direction]
        ni, nj = i + di, j + dj
        # add new point with new coordinates, direction to calculate the entry direction and distance from the start
        queue.append(((ni, nj), (di, dj), distance + 1))
        track_maze[i][j] = PRINT_DIRECTION[di, dj]

        if (ni, nj) == previous_point:
            track_maze[ni][nj] = "*"
            return distance + 1, track_maze
        previous_point = (ni, nj)


if __name__ == "__main__":
    maze ="""F--F7F7|7FJ..JF-7F|77FL-L7.L.L7LFFJ-77|7.L777LF7L|FJJ-7-F|J7-7FF-7..FFF7JF--L77FL--77-7-77-|7FJ.LL.|7L7-|-FJJ.-J.F-77|F---|7.F--|--.F-7-7.F7
FJ-|J|JJLF7F77|||FJ7J-|J|LF7.L||LJ|L77LL-JL--F--.LLJ|-..7|FJ..FJ7F.J.|7L-L7.|--F.7J||L|J.JJLFJF77|-LJ-|-J-FJ-F|J|-7|-L|JJ.L7.|-F77-FFJLLF.L-
.||..|J.-|-JL777LJLF7LF7FFL-7-F7.F--LF7||FL.|JJ|F7J.-J.|LJ--7-JLFJ7.7L7|F7LJ7J|LL|FF|.|-7L|F7JL-LF-L7LJJ|L|7.L|-FJLLJLL-F|JLJ7JLJJ-FJ7J-LFL7
F7--|L|7|FJLL7-L7L7.|LJJJ.|F77||.L-JF|-7J.||.|JF||-|J|F|-||FF7.L.FF-L7L|L-7L--|-L|J|L--7F7F|....FL7L777F7L|J--.F77JJ|.LFJ|J.LJ.F|F7LF-.F7JF|
.--FJ-J--J7.LF-LJLFFJF|.||F-.FJLF7.F7LF7|F|7.FF7|||L-7F|-J7F||7.7J|7.|.L-.FL|L|7--7L77L|LL|J-7FFJ-|JLF-J|7|-7JF||JF7|7F|---77---JL7.-JFLF.-|
JJ.|7.|-FL-7F--FJ-LL-7--L7-77J-FJ|-F--J|F7LF|7||||7F7.JJ..FFJL7J.FJL.||F|7J.L-L7-LL-|7L|.||7.|F---J-JL-7L7F-7-L||LJJ-J.LFJFJ7F|7FLFF|-FF77-|
F--J-LJ-7|.|J-F7J7JL--7.|||-7.LL7|-L7F-J|L-7LFJ||L-7F77FF7FJF-J|-|F|.FFJ7|--||J|..|-77-J-F|-J7|JJFL77L|L7L7||LL|L7LL7F-7|.FJ|FJFL..LL7..|7FF
JFFJ7.|-JJ7LJF-J|L-77.L-F-7-FF-7||-FJ|FFJF-J-L7||F7||L-7|LJFJ|.7.FF7-7|LF|7--7FFL-|-F77.-F7-|F77-L|F--7|L7L-7LFJFJF7-|.J.FLJFF-L|7-7LJJ7LJ-|
F-7JF7.L|--.|7.|7|-JFFFFJFJ.LL7||L7L7|7L7|L|F7|LJ|LJ|F-JL-7|F7..FLL7LFJ-||JFF|--.||L|L77F||LFJL77JLL-7L7FJF-JFJFJ-||FLJ-F7|-7JJJ|7F|-J7|-J|F
7.J.-JF.J.F7-JFFFJ.LJ-FL7|F7F7|LJFJFJL7FJ|F7|||F-JF7|L7J7||L-77LF7.J-|..|-7F7|F|.FF7|FJ7FJL7|F-JJ77F7|FJ|FJ7-L7L7FJL77|.|JL7J-7-JJFJ7--JF.FJ
FJ7L7.|-FL-L-F|LLF7-J.FFJ|||||L-7L7L7FJ|FJ|LJ|||F-J||FJFF-JF-J7L-J7L||L-7.-||FF7F-JLJL-7|F-J||JF7F-JLJL-J|F7F7|FJ|F-J77|-77L..J-J7|.JLL7FF7|
--JF-JJLJFL|-F77J|LF-F7L7|||||FFJFJ-|L7|L7L-7LJ|L7FJ|L7FL-7|F7J-L|LFF|.L|7-||FJ||F7F--7|||-FJL7||L7F7F--7LJ|||||-||F7F7J.L7LLJJJLJFJL7J.F|J7
|.LF|JF|L7.L7|||.7-F-|L-J|||||FJFJF-JFJL7|F7L7FJFJL7|FJF-7||||7..|---F77FF7||L7|LJLJF7|||L7|F-J||F||LJF7|F-J||||FJLJLJ|F7LFJ|.F.|FJ|LL.F-JFJ
|J.7.|L--J7FJ|7LFL7L7L--7||||LJFJ.L7FJ|L|LJL-J|FJF7|||FL7||||L7F7JF|-||F7|LJ|FJ|F7F-J||||FJ||7FJL7LJF7||||JFJ||LJF7F7FJ-|J..77L|-L.7FF-J||FJ
|-LJ-7|L|7-|L-7--L7|F77FJLJLJF-JF7FJL-7-L---7FJ|FJLJ||F-J||||FJ|L--7FJ|||L7FJ|FJ||L-7LJLJL-J|FJF-JFFJLJLJL7L7||F-JLJLJ|L7FF7JFJLJ|-J-7--FJJF
|J.LLL--F77|LF-.LLF-JL-JF---7L-7||L7F-JF7.F-J|7|L-7||||F-J|||L7|F--JL7||L7||FJ|FJ|F7L---7F7FJ|FJ|F7L7F---7L7|LJL--7F--7.L-7LLJJ|L|7F7L--|.F|
7-L-7L-JL-L7L||.LLL7F---JF7FJF-J||FJL7FJL7|F7L7|F-JFJ||L-7||L7LJL7F7FJ|L7||LJFJL7|||JF--J|LJFJL-7|L7LJF--JFJ|F----JL7FJFLF...|FJ-7-FJ||..FJ|
||.LJFJLL-JF7JF7FF7LJ-F7FJLJFJF7||L7FJ|F-JLJ|FJ||F-JFJL7FJ|L7|F--J|||FJFJLJF-JJFJLJL7L--7|F7L7F-J|FJJ-L--7|FJL-7F7F7||F77L|7.77.LFJ|-L|F7|--
F7LL-777|-|F77F7FJL7F-J|L--7|.|LJ|FJL-J|F-7FJL7||L-7|F7|L7L7LJL-7FJ|||7L-7FJF-7|F-7FJLF-JLJL7||F7|L7LF7F-JLJF--J||||||||L7-FJ.|L-.F|7F7-L--J
F|.|-F-|7.F|L-JLJF-JL-7||F-JL7|F-J|F---JL7|L-7|||F7|||||FJJL-7F-J|FJ||F-7||FJFJ|L7LJF7L-7F--J||||L7L7||L-7F-JF77|LJLJ||L-77JLF|JFFLJF7.L|F|.
7JF7|JL|LFFL----7L7FF-JL-JF-7||L7FJL-7F7FJ|F7|LJ||||LJLJL-7F7|L--JL7||L7LJ|L7|FJFJF-JL--JL7LFJLJ|||FJ||F7||F-JL7|F---J|F-JJLFF777F.LLLJ-J-J|
J|L.-7|L7|||L7F7L7L-JF7F--JFJLJFJL7F-J|||FJ||L-7||||F--7F-J|||F----J|L7L-7L-J|L7L7L-----7FJFJF--JFJL-JLJLJ||F--J||-F--JL7|7F7||JJ|FLL|.|-F-J
LJ-|LJ-JFJL|-FJL7L---JLJF7FJF--JF-JL7F|||L7||F-J|||||F7LJF7|||L--7F7L7|JFJF--JFJFJF-7F--JL7L7L7F7L-------7|||F7FJL7|F-7FJF7|||L77LJ7.L-7.|L7
F|7L7J-FJ-LJ|L-7|-F----7||L7L--7L--7L7||L7LJ|L-7||LJLJL7||LJ||F--J||FJL7L7|F7JL7L7L7LJF-7FJFL7|||FF7F7F--JLJ||LJF-J||LLJFJ||||FJ7JJJFJFLFL-|
|-JL|7LF7-FLF-FJL7L---7LJL-JF--JFF7L7||L7|F-JF7||L7F--7L7L-7|||F77||L-7L7|||L-7L7L7L-7|FJL-7FJLJ|FJLJ|L----7||F7L7J|L7F-JFJ|LJL-7..FF-L.|J||
L-F7--FJF7-F7FL7FJF7F7L----7|F7F7||FJ|L7||L7FJ||L7|L-7L-JF-JLJLJ|FJL--JFJ|||F-J7L7|F7||L7F-JL7F-JL--7|F7F-7||||L7L7|FJ|F-JFJF--7L77J|.LL|-7.
J.-7-FJF|L-J|F-JL7|LJ|.F7F7|LJ|||||L7|FJLJFJL7|L7LJF-JF-7|F----7||F7F-7|FJLJL-7F-J|||LJFJL-7FJL7F7F-JLJ|L7LJ||||L-J|L-JL--JFJ.LL7|||F7F||F-7
FL-L-F7LL--7|L--7|L-7L-JLJLJF-J||||FJ|L7F-JF-JL7L7FJF-JFJLJJF7-||LJLJ.||L7F---JL7FJ|L7FJF--JL-7||LJF7F-J.L-7LJL-7F7|F------J-FJLLJJF|JF|-7F-
|FF7.L7JFLFJL-7FJL7JL------7|LFJ|||L7|FJL7FJF-7|FJL7|F-JF7JFJL-JL7F7F-J|FJL-7F7FJL-JFJL7L7LF7L||L7FJ||F77F7|F7F-J|||L-------7F7F|.|-77L-JLFJ
LLJLJ7J.F7L--7LJF7L-7F-----JL7L7||L-J||F-J|FJFJ||F7LJ|F7|L7L---7FJ||L-7LJF--J|||F---JF7L7L7|L-JL7LJFJ||L7||||LJF7|||F-------J||F--77|7-L.F-J
7.L7L|F7|||F7L--JL7FJL---7F-7L7||L-7FJ|L-7LJ|L7|LJL7FJ||L7L7F--JL7||F-JF-J7F7|||L7LF7||L|FJL--7FJF7|FJL7LJLJ|F-JLJLJL-7F---7FJLJF-J-|7.JFL-7
L7.77|JFJL-JL-----JL---7LLJFL7LJL--JL7|F-JF-7FJL7F7||FJL7|FJL---7LJ|L7FJF-7||||L7L7|LJ|FJL7F7FJL7|LJL-7|F---JL7F--7F-7LJF-7LJF--JJL|L7777-FJ
FLFF7LLL7F-----7F---7F7L--7F7L7F----7|||F7L7|L7FJ|||LJF-J||F7F7-L-7L7||J|FJ||||FJFJ|F-JL-7|||L7FJL--7FJ||F7F7FJL-7|L7L7FJFJF7L--77-JJJLJ--|7
77.LF7F-J|F----J|F--J|L7F7LJL-J|F---J||LJL7||FJ|FJ||F-JF-J|||||F7LL7LJ|FJL7||||L7L7|L7F7FJLJ|FJ|F-7FJL7|LJLJLJF7FJL-JLLJ|L-JL-7FJF7-L-7|||L|
|7F-F7L--JL----7||F7FJ||||F7F--JL---7||F--J||L7||FJ||F7L7FJ||||||F7L-7|L7FJ||||7|FJ|FJ||L7F-JL7||FJL7FJ|F-----JLJLF7F----7|F7-LJL||F7LF7F--7
F.7||||F7F7|F7FJ|||LJF-J|||||F--7F--J|||F7FJL7|||L7|LJ|FJL7||||||||F7||FJL7||||FJL7||FJL7||F7FJ||L7FJL-JL----7F--7|||F---JFJL-7F-J||L-J|J|||
.7JF|L-JLJL-JLJFJLJ7FJF7|||||L-7|L-7LLJLJ||F-J|||7|L-7|L-7||||||||||LJ|L-7LJ|||L7FJ||L-7LJLJ|||LJFJL7F-------J|F-J|LJL--7LL7F7|L7FJ|F--J77-F
LF.LL7F-7F7F-7FJF7F-JFJLJLJLJF-J|F7L---7|LJL-7|||FJF7||F-J||||||||LJF-JF7L7JLJ|FJL7|L7FJF---JL7F7L7FJ|F7F7F7F7||F-JF---7L7FJ|LJFJ|.|L-7JFJFF
|.--L||.LJ|||LJ-||L--J7F7F7F-JF7LJL---7L--7F7|||||FJ||LJF-J|||||LJF7|F7|L7L--7LJF7||FJL7L7F-7FJ|L-J|-LJLJLJLJLJLJF7L--7L7||FJFLL7L-JF-JF77LJ
|FL|F||F--J|F7F7||F77F7|LJ|L--JL7F---7L---J|LJ||||L7|L-7L7FJ|||L7FJLJ||L7|F-7L7FJLJ||F7L7|L7|L7L7F7L7-F7-F7F-----JL---J7LJ||F7F7|F--JF-JL7J7
J-FF-LJL7F7||LJLJLJL-JLJF-JFF7F7LJ.F-JF7F7JL7FJ|||FJ|F7L7||FJ||FJ|F-7|L-JLJFJFJ|F-7||||FJL7||FJFJ|L7|FJL-JLJF--------7F7F7|||||||L-7-L7F-J-J
|FFF-F-7LJLJL7F--------7|.F7||||F--J|FJLJL-7|L7||||FJ|L-JLJL-J||FJ|FJL--7F7L-JFJ|FJ|||LJ|FJ|||FJFJJLJL----7FJF------7LJ||||||LJLJF7L7L|L7L|J
|-||FL7|F-7F7LJF-------JLS||||||L----JF7F7FJL-J||||L7L-7F7F--7|||FJ|F7F7LJL--7L7|L7||L-7FJFJ|||FJF-7F7F---J|FJJF--77L--J|||||F--7|L7L-JFJ.J7
F-|-F-J|L7|||F7L--------7LJLJLJL7F----JLJLJF--7LJLJFJF7LJ||F7LJ|||FJ|||L7F7F7L7||7LJL7FJL-JFJ|||.L7|||L----JL-7L7FJF77F7|||||L-7LJ-|F--JF7|L
|7|FL-7L-JLJLJL-7F7F7|F-JF7F-7F7LJF7F------JF-JF-7LL7||F7|LJL7FJ|||FJ||FJ|LJ|FJ||F---JL---7L-J||F-JLJL--------JFJ|-||FJLJLJLJF-JLF7LJF7F77F|
FF----JF7F-7F7F7LJLJ|FJF7|||-LJL--JLJF7F---7L-7|FJF7LJ||LJF--JL7|||L7LJL7L-7||-||L--7F7F--JF-7LJL------7F7F-7F7L7L-JLJF-7F7F-JLF7||.FJLJ|7F7
LL-7F7FJ|L7||LJL---7LJFJLJLJF7F7F----JLJJF7L--J||FJL-7|L7LL--7FJLJ|FJF7F|F-J|L7LJF--J|||FF7L7|F7F7F7F-7LJLJFJ|L7|F----J|LJLJJF7|LJL-JF-7L--7
|LJ||||FJFJLJF77F--JF7|7F7F7|LJ|L----7F-7|L--7FJLJF7FJL7L7F7-|L--7LJJ|L-JL7FJFJF7L7F7||L-J|FJLJLJLJ||FJF7F7L-JFJ|L-7F7F7F-7F-JLJF-7F-JJL7F-J
|.F||LJL-J-F-JL7L---J||FJ|||L-7|-F7F7|L7||F7FJ|F--J|L77L7||L-JF7FJF--JF7F-J|FJFJ|FJ|||L7F7|L7F7F7F7LJL-JLJL7F7L-JF-J|||||FJ|F--7L7LJF77LLJJ|
FJ-LJ.LF---JF-7L----7LJL7LJL--JL-JLJ|L-JLJ|LJFJL--7|FJF-J|L-7FJLJ7L7F7||L-7|L7L7LJFJ||FJ|LJFJ|||||L7F--7F-7LJL7F7L--JLJLJL-JL7JL-J|FJL7J|FF7
FJLLL-LL7F7FJFJF7F-7|LF7L--------7F7|F7F-7L--JF7F7|LJFJF7L7FJ|7F--7||LJ|F-JL7L7|F7L7||L7L-7L7|||LJFJL7FJ|FJF7FLJ|F7F---------JF7LF7|F-JF7F7|
L--|....LJLJFJFJ||FJL-JL---7F7F7FJ||LJLJLL--7FJLJ|L-7L7||FJL7L-JF-J||F-JL--7|FJLJL7||L7|F7L7LJ|L7FL--JL-JL-JL7F7LJ|L----------JL-JLJL--JLJL7
||L7--|.|-L|L7|FJ|L-7F7F--7LJLJLJFJL-7F7F--7LJF7LL--JFJ||L7-|F--J|FJ|L7F7F-JLJLF-7||L-JLJ|FJF7L-JF7F---7-F---J|L-7|F7F7F-7F-7F--7F7F7F--7F-J
FJ-LJ.FF-7.F7LJL-JFFJ|LJF7L-7F7F7|F--J|||F-JF-JL7F7F7L-J|FJFJL---7|FJFJ||L-77F7L7LJL----7LJFJL-77||L--7|FJF---JF-JLJ||LJ7LJFJL-7|||||L-7||JL
L.F.|.LL7L----7LF--JFJF-JL--J|||LJL---JLJL-7|F-7LJLJ|F-7||FJF7F7FJLJFJFJ|F7|FJL-JF-7F7F-JLFJF-7L-JL--7||L-JF7F7L--7||L----7L7F7|LJLJL--JLJ77
F|JF7-FFJF-7F-J-L7F-J|L---7F7|||F---7F7F7F-J||.L-7F-J|FJLJL7|||||F7FJFJ7LJLJ|F7F7|FLJ|L7F7L-JFL7F7F-7LJL---JLJL7F7L7|F-7F-JFJ||L7F7.LL|J|.L7
LJ.|L-LL-J-||F7F7LJF-----7LJLJLJL--7LJ|||L--JL7F7LJF7|L7F7FJ|LJ|LJ|L7L---7J-LJ|||L-7JL-J||F-7F7LJLJFL-7F------7LJL-JLJFJL-7L-JL7LJL7.|J.FL77
|J.7F||L|F-JLJLJL-7L----7L---7JF--7L-7|||F-7F7LJL7L|||FJ||L7L-7|F7||L7F--JJ7.LLJ|F-JF---JLJFJ||-F7F---J|.F7F-7L--7F--7L---JF7F7L---J-7.FL|L|
LFJJ-L7FFL7F7F---7|F-7F7L---7L7L-7|F-JLJ||FJ|L7F7L-JLJL-JL7L7FJ|||L7FJL--7-7FF7FJL7JL-----7L7||FJLJF--7|FJLJ|L7F7LJF7L7F---JLJL---7.||F7FJLL
F|J7LJ.|JFLJ||F-7||L7LJ|F7F7L7|F7|LJF7F7LJL7L7|||F---7F-7FJ-LJFJ|L-JL7F--J7LFJ|L--JF7|F7F-JFJ||L---JF-J|L---7FJ|L7FJL-J|F-7F--7F--J.|L|L-J.|
F|F77-JL-LJFJ|L7LJ|.L-7||LJL-J|||L--JLJL7F-JFJLJ|L--7||FJ|-7.LL7L7F--JL-777.L7|F7F7||FJ||F7L-JL-7F--JF-JF---J|FJFJ|F---JL7|L-7LJJ.LF--L7F|F-
JLL-77..L|7L-J-L-7L---JLJF---7|||F7F7F-7|L7FJF--JF-7|||L7L7LLLFJFJL-7F--JJFF-JLJLJ|||L7|||L-7F-7LJF--JF7L--7|LJ|L7||F7F7FJ|F7|7LJ-FJJ.L7-LJJ
.7LJ|L7-|F-----7.L----7F7|F7FJLJLJLJLJ.LJ7||JL--7L7LJLJ-|FJ7J.L-JJ.F||JLLJFL---7F7LJL7||LJF-JL7L7FJF--J|.F7L7LF7-LJ||LJLJ7LJLJ-.LFL7.|-JJ-LF
F||.F-F7FL----7L---7F7|||||LJF-7F7F----7F7LJF--7L7L----7||J7-7||.-F-JL7||F7FF7FJ|L--7LJL-7L7F-JLLJJL7F7L-JL-JFJ|F7FJL--7F7F-7FJ.7J--LL-J..F-
-JF-F7J7F.F7F-JF--7LJLJ|LJL--J.||||F---J|L--JF7L7L7F-7FJLJ7J.L|7-LL---J-F||FJ|L-J7F7L--7FJJLJF7F---7||L7F7F-7L7||||F---J|||FJ-7F|7.|LJFF7FLJ
|L7-|L7-F7||L--JF7|F7F-JF-----7LJLJ|F---JF---JL-JFJ|FLJF7F7F77J|||F|-F|7F||L7|F7F7|L-7FJL7F-7||L-7FJ||FJ|||FJFJLJLJL7F--JLJL7||7|F|JLLLFJ..|
-F||L7L-JLJL7LF-JLJ|LJF7L----7|LF-7LJF---JF-7F--7L7L--7|||||L7FF7-FF7JJ-FJL-JLJLJLJF7|L-7LJFJ|L7FJL7||L-JLJL-JF-7F-7LJF-----J7|F7F7-7|||J-F|
||JFJL7F7F-7L7L---7|F-JL-----JL7L7|F7L----JFJ|F-JLL---J|||||FJ7F7.F7JL7FJF-7F-7F7F7|||F-JF7L7L7|L7FJLJF----7F7L7LJ7L-7L-------7F7||F---77.LF
-JJ|-FJ|LJ.L7L-7F7||L-7F-7F-7F7L7|LJL---7F-JF||F7F7JF-7|LJLJL--JL-JL7.FL-JFJL7||LJLJ|LJF7|L7L-JL-J|F7FJF--7||L-J|F--7L---7F--7||LJ||F--J.|J|
FJ7LFL7L7F7JL-7LJ|LJF-J||LJFJ|L7LJF----7|L--7||||||FJFJL7F---------7|-L7JF|F-JLJ-F--JF7|LJFL--7F-7LJLJFJF-JLJ|F7FJF7L---7||F7LJL-7||L7-L7.F|
L-L--FJFJ||7F7L-7L--JF7|F--JFJLL7FJF7F-JL---J|||||LJFJ|FJL-7F-----7LJ7LJ|FJL7F---JF7FJLJF7F---JL7L7F--JFL7F7JFJLJFJ|F---J|LJL7F-7|||FJ7F|7F|
|7|-LL-JFJL-JL--JF---JLJL---J|FLLJF|LJF7F7|F7|||LJF-JF7L7F-J|F-7F7|JJ|J.FJF7|L---7|LJF7FJLJF7F--JFJ|F---7LJL-JF7FJFJL-7F7L---J|FJ|LJL7F777L7
|-7-LLJF|F7F--7F7|F7-F7F--7F-7-F7F7L-7||||FJLJLJF7L--JL-JL--JL7|||L7.|7.L-J||JF7-LJF-JLJF-7|||F-7L-J|F-7|F-7F7|LJ||F-7LJ|LF7JFJL7|F-7LJL-7JJ
L..F7JJFLJLJF7LJLJ||FJ|L-7LJFJFJLJL--J||||L7F-7FJ|F7F-7F--7F--JLJL-J.L|7L|JLJFJ|F--JF-7FJ|||||L7L-7.LJFJ|L7LJ|L--7LJLL-7L7|L-JF7LJL7|F-7FJ7|
|--7JLFL|-F-JL7F7F||L7L-7L7FJFJF------JLJL-JL7LJLLJLJFJL-7|L--------7L|-L|J|-L7|L-7FJFJ|FFJ|||FJF7L7F7L7L-J.FJF-7L----7L7LJF--JL7F-JLJLLJLF7
L--JJF|7JLL--7|||FJ|.|F-JFJL-JFJF--------7F-7L-7F---7L---J|F7F-7F---J.|JL7-JJFJL--JL7L7|FJFJLJ|FJL7LJL-JF7F7L7|LL-7F7FJL|F7|F--7|||F7-||.|L|
7-|.FL7F7-F7FJLJ|L7|FJL--JF---J.L-------7||FJF7LJF-7L----7LJLJLLJJL|FFF7FJ||.L---7F7|FJ|L-JJF7LJF7L-7F--JLJL7|L--7LJ|L-7|||LJF-J|L-JL77JF|-F
LF7FF7|.F7||L7F7L-J|L-----JF------------JLJL-JL-7L7|F-7F7L-7F-7|J..LF-J|-|-7J-F--J|LJL7|F7F-JL--JL--JL7F----JL--7L-7|F7||||F7L-7L7F--J|.FJ|L
L-JF-F7FJLJL-J|L--7|7F---7JL---7F--------7F----7L-J|L7||L--JL7|7LJ..L7FJ.F-7J7L7F7L7F7LJ|LJF7F-7F7F-7FJ|F7F---77L--JLJLJLJ||L--JFJL--777|J|7
.|FFJ||L------JF--JL-JF-7L7F---J|F------7LJF--7L--7L-JLJF7F7.|L77.77F|L-7L7L7F-J|L-J|L--JF7||L7LJ||FJ|FJ|LJF-7L7F-7F-----7|L--7FJF-7FJ.J77F|
FFF7-|L7F-----7L--7F-7|JL7|L-7F-J|F----7|F7L-7L---JF7F-7||||FJFJF7F7-|F-JF|FJL--JF--JF-7FJ||L7|F-J|L7|L-JF7L7L7LJFJL7F---JL---JL-J-LJJ.|.|-J
-F|L-JFJL----7|FF-JL7||F-JL7LLJF7LJF-7FJLJL--J7F7F7||L7|||||L7L-J||L-J|F7FJL---7LL--7L7LJF|L7LJL-7|7||F--JL7L7|F-JF-JL---7F7F7.F----7J|-FL7J
|||F-7L7|F7FFJL7|F7FJLJL7F7L--7||F7L7LJF7FF-77FJLJLJL7|||LJL7|F--JL--7||||F----J-F-7L-J7F-JFJF---JL7LJL---7|FJ|L-7|F----7LJLJ|FJF---JF-J.||J
FFLJ-L7L7|L-JF7LJ|LJFF-7LJL7F7LJLJL-J|FJL7L7L-JF-----J|LJF--J|L--7F7FJLJLJL----7JL7|F---JF7L7L7F---JF7JF--JLJ.L-7LJL--77L----J|FJFL.|-L7--J|
|J|-F7L7|L-7FJL--J7F7|FJF7FJ||F7F7F7|FJF7L-JF-7L----7FL-7|F7JL7F-J||L--7F------JF7||L7F-7|L-JFJ|F---JL-JF7F7F7F7L7F--7L7F7F-7-|L-7.F|7.|.LFL
-F--J|-||F7LJ-F-7F7||||FJ|L-JLJLJLJL-JFJ|F--J.L-7F--JF--JLJ|F7||F7||F7FJL7F7F7F7|LJ|.LJLLJ|F7L-JL-------JLJLJLJL7|L-7|FJ||L7|FJF7L-7JJFF7777
FL--7|FJLJ|JF7L7LJLJ||||FJLF-7F7F7|F-7L7|L-----7LJF-7L--7F-J|LJ||||LJ|L-7LJLJ|||L-7|F7F-7F-JL7F-----------7F----JL7FJLJJ|L7||L7|L--JF7F|L77J
-LF-J||F-7L-J|LL---7LJ|||F7L7||LJL-JF|FJL--7F--JF7L7|F7FJL77|F-J|LJF-JF-JF---J|L7.|||||FJL-7FJL7F----7F--7LJJF7|F7LJF7F7|FJ||F|L-7F7F7FJFJ|7
.LL-7|LJJL--7L----7L-7LJ|||FJ||F----7|L---7|L-7FJL-J||||F-JFJ|F7|F-JF7L-7L7F7FJFJFJLJLJL-7FJL7LLJJF--J|F7L--7|L7|L7FJ||||L-JL7|F-J|||LJFJJJ-
L7JFJL-7F---JF-7F-JF7|F7||LJFJLJF-7FJ|F7F-JL--JL-7F7LJ|||F7L7|||||F7||F7L7|||L7|.L-----7FJ|F-JF---JF--J|L-7FJ|FJ|FJL7||||F---J||F7|||F-JJ7JJ
F7.L--7|L-7F-JF||F7||LJ||L-7|F7JL7|L7||LJJF----7JLJL7FJ|LJ|FJLJLJ||||LJL7|LJ|FJ|F7F7F7FJL7||F7L----JF7FJF7LJ.|L-JL-7|||||||F--JLJLJLJL-7||.-
L|FF--JL--J|F--JLJ|||F-J|F7||||F7|L-J||F--JF7F-JF--7|L7|F-JL--7F-J|LJF--JL7FJ|FJ|LJLJ|L7FJ|||L7F7F--JLJFJL--7|F7F--J||||||FJF7F7F-7F-7FJJJ|J
LF-JF7F----JL----7LJ|L-7LJLJLJLJLJF7F||L7F-JLJF7L-7LJFJ|L7F7F7|L7FJF-JF-7F|L7|L7L---7|7||.|LJFJ||L-----JF---J||LJF7FJLJLJLJFJLJLJ-LJ-LJFL-J-
.L--J||.F--------JF7L--JF7F-----7FJL7||FJL---7|L-7L-7|FJFJ|||LJFJL7|F7L7L7|FJL7L7F7FJ|FJL7L-7L-JL7F7F--7L--77|L7FJ|L7F--7F7L7F--7LF77F7F7F-J
FF77.LJFJF-7F---7FJL-7F7|||F----J|F-JLJL7F---JL7FJF7|LJFJL|||F-JFFJ|||7|FJ|L7.|FJ||L7||F-JF-JF--7LJ|L-7L--7L-JFJL7L-JL-7LJL7||F-JFJL-JLJ|7J|
FJL---7L-JLLJ.F-J|F-7||||LJ|F-7F-JL7F7F7|L-7F-7|L7|||F-J-FJLJL7F7L7|||FJL7|FJFJL7||FJLJL77L--J|FJF7L-7L--7|F-7L--JF-7F7L7F-JLJL--JF7F7F-J-FL
L----7|F7F----JF-JL7|||LJF-J|7LJ7F-J|LJLJF7||FJL7||LJL7F7L7F--J|L7|LJ||F-J||FJF-J||L---7L7F-7F7|FJL-7L7|FJLJF|F--7L7LJL-JL--7F7F--JLJLJ.|.|J
FF---JLJLJF7F-7|F--JLJL-7L7FJF---JF-JF---JLJ||F7||L--7LJ|FJ|F7LL7|L-7LJ|F-J|L7L-7||F-77|FJ|FJ||LJF7JL7L7L---7|L-7L7|F7F7F7F-J||L-----7F7-7.|
L|F7F7F7F-JLJFJ|L----7F-JJLJJL----JF-JF-7F7FJ|||||FF7|F-JL7LJ|F7||F7|F-JL-7|FJF-J||L7|FJL-J|FJL7J|L-7L7L--7FJ|F-JFJLJLJLJ|L7FJ|F-7F-7LJ|JLJJ
LLJLJ||||7F--JFJF----JL-7F--------7L--JFJ|||FJ|LJL7|LJ|F7FJF-J|LJ||LJL7F7FJ|L7L--J|FJ|L7F7FJ|F-JFJF7L7L7F7|L7|L-7|F-7F---JF|||LJJLJJL--J-JJ|
-7L|LLJ||FJF7FJLL----7F7|L--7F---7L----J7|LJ|FJF--JL-7||||FJF7L-7LJF--J|LJFJFJF---JL7L-J|LJ|||F7|FJL-J.LJ||FJ|F7|||FJL----7|L----------7JJ.|
FFJ.FF-J|L7|||F-7F--7LJLJF--J|F-7L-----7FJF7|L7L7F7F7|LJ||L7|L-7L7FJ7F7|F7|||FJF7FF7L--7L7F7|||||L7LF7F--JLJ|LJLJLJL7F7F-7||F-7F---7F7FJ.L-J
||7-FL7FJLLJ|||FJL-7|F7F7L-7FJL7|JF----JL7|LJFJFJ|LJ|L-7||FJL-7|7|L-7||LJ|L7|L7|L-JL7F7|FJ||||||L7L7||L--7F7FF-7|F7L||LJFJ|||-||F7JLJ|L77J.|
JJ7.|.LJ|F--J||L77FJLJ|||F7LJF-JL7L---7F7||F7|FJ-|F-JF-JLJ|F7FJL7L-7||L7FJFJ|FJ|F7F-J|||L7||||||FJFJ|L-7FJ|L-JFJFJL-JL77L-J||FJLJL-7JL-J--|7
|-J-7-LLLL---JL7L-JF-7LJ|||F7L--7L----J||||||||F7||F7L--7FJ||L7FJF7|||FJL7|||||||LJF7|||FJ||||||L7|JL-7|L-JF7FJJL--7F7L7F7|LJ|F-7F-J7J.|7..J
|.|7JFLJ|F----7L7F7L7L-7LJLJL---JF7F-7FJ|||||||||||||F-7||FJ|FJ|FJ|||||F-JL7|L7|L7FJ||LJ|FJLJ||L7||F7FJL7F-JLJJFF7FJ|L7LJL-7FJ|FJ|F7|F777F-J
.F77--7-L|F--7L-J|L7|F-JF--7F7F-7|||FJL7||LJLJ||||||||FJ||||LJFJL7|||||L--7||L|L7||FJ|F-J|F7FJ|FJ|||||F-JL-7F7.FJ||FJJL7F--JL7|L7LJL-JL7--J|
FF-7-LF-7LJF7L--7|.LJL--JF-J|||FJ|||L7FJ||F---J|||||||L7||L-7FJF7|||||L7F7|||FJFJLJL7|L-7LJ|L-JL7||||||F7F7LJL-JFJ|L7FFJL--7J|L7L7F7F7FJ.|7-
LJ-|77F.F--JL---JL7-F7F--JF7|LJL7||L7||FJ||F-7FJ|||||||||L7FJL7|||LJ||-||||||L7L-7F7||F-JF7L-7F-J|LJLJ|||||F7F-7L7|FJFJF7F7L7|FJ7||LJLJJ7..|
|JF77LF-JF7F----7FJFJLJF7FJLJF--J||FJ||L7|||FJL7||||||FJL7|L7FJ||L-7LJFJ||||L7L7FJ|LJ||F7||F7||F7L---7||LJ|||L7|FJLJFJFJ|||FJLJFFJL7J.J.|F-J
-.LJJ.L7FJLJ.F--JL7|F7FJ|||F7L-7FJ|L7||7||||L7FJLJLJLJL7FJL7|L7||F7L-7|FJLJL-JFJL7L7FJ||||||LJLJL7F-7||L-7||L7||L--7|FJ.||LJF7LLL7FJ-||.FF|J
.-F|JLLLJL|LFJF7F7|LJLJFJ|FJ|F-JL7|FJ|L7LJLJL||F7F7F---JL-7LJ|LJ|||F7||L7F----JF7L7LJ||||||L7F---JL7|||F-J|L7|||F--J||F7|L--J|.LLLJJ7LFLFJLF
--LFJFLL7|JFL-JLJLJ.F--JFJL7|L7F7||L7L-JJF7.FJLJLJ|L---7F7|F7FF-J||||||FJ|F7F-7|L7L--7LJ|||FJL---7FJ|||L-7|FJ|||L--7|LJ||F--7L-7JJ7.FFJ.-F-J
|.|.F7|LJ7.LJL|JF7F7L-7FJ7FJL-J|LJ|FJ-F--JL-JF7F-7|F---J||LJL7|F7|||LJLJF||||FJ|FJF-7L7FJ||L7F---JL7|||F7|LJ|LJL7F-J|F-J|L-7|F-J|JF|JL-JFJ||
F7J7FFFJ|-.L7.|FJLJL-7LJF7L-7F7|F-JL7FJF-7F7FJ|L7||L7F-7||F-7|LJ|||L-7F--J||||FJ|FJFJFJL-J|FJ|F7F7FJLJLJ|L--7F--JL-7|L-7|F-J|L-7F7LFJFF|L-|7
-|F|L|J-L77LFFFJF-7F7L--JL--J|LJ|F7FJ|FJFJ|||FJFJ||FJL7|||L7||F-J||F-JL7F-J|||L7|L7L7L---7LJFJ||||L----7|F--JL--7F-JL7FJLJJFJF-JJ-7JF|7|JFJ-
.L-J.||LJJ|F|.L7|JLJL7F-7F--7L7FJ||L7||-L7|||L7|7|||F-J|||FJ||L7FJ|L-7FJL-7LJ|FJ|FJ7L-7F7L-7L7|||L7F-7FJLJ-F-7F-JL--7||F7J7L7L7-F-J-|.F|-|.|
-.LF-LL7.FFJF7L||F7F-J|FJ|F-JFJL7||FJLJF-J|||FJL7|||L-7|||L7||FJ|FJF-J|F7FJ7FJ|FJL-7-FJ||F7|FJ||L7|L7|L----JFJ|F7F-7||LJL-7L|FJ-JJJJ|F|-7L77
L-FFJLL-.L|FL7LLJ|LJF7|L7|L7FJF-J|||7F-JF7||||F7|||L-7|||L7|||L7|L7L-7|||L-7|FJL7F-JFJFJ||LJL7||FJL-J|F7F---JFLJ||7LJ|F--7L7||FLJ.F-J7JF7.--
LJ|...|J|-|--J777|F7|LJ.LJFJL7|F7|||FJF-JLJLJ||||LJFFJ||||LJ||FJ|FJF7|||L7FJ||F-JL7FJFJFJL7FFJ||L7|F7|||L-----7FJL--7|L7J|FJ||JLF-J.FJ7|7L7|
J-JJ7.--|-|||7FF7||LJ.FF--JF-JLJ||||L7|F7F7.FJ||L--7L7||L--7LJL-JL7|LJLJFJL7||L7F7|L7|FJF7|FJFJL-JFJLJ||F7F--7|L---7||FJJLJFLJ77J-LJJL7.-.||
|.|--7-|LJLLJ-FJFLJJ--FL7F7L7F77||LJFJ||LJL-JFJ|F7FJL||L7F7L7F----JL---7L7FJ|L7LJLJFLJL7|||L7L--7FJF-7|LJLJ7FJL---7||||FLJL|-|7F7F7J|-J7J-||
FFJFJ-F|J.||L|.F--|J.FF-J|L7LJL7|L77L-JL--7F7|FJ|||F-J||LJ|FJ|F7F-7F---JL|L7L7|F------7|||L7|F7FJL-JFJL7F7F7L--7F-J||LJ7JFFFJL7|FL---7|7..FF
7J-FJ.||-JLL-77JL-..--L--JFL7F-JL7L-7F----J|||L7||||F7L-7FJ|FJ|||FJ||F--7|FJFJ||F--7F7LJ|L7|LJ|L---7L-7||LJL--7LJJLLJ.|||FJJ|FJ7J.L|LLF-7-7J
L-7JFF||LL7LFJLF7.FFJ.LF7F7FJL--7L-7|L----7|LJFJ||||||F7||FJ|FJ||L7L-JF7|LJJL7|||LFJ|L7FJFJ|F-JF--7|F-JLJF--7FJJ7|FJ-F7JFJ-FLJ-J7|-JJ.-J|L|L
LJJJFJ.|-JL7LJ7L--|LLLFJLJLJF--7L7L|L7F---J|F7L-J||||||LJ||FJ|FJL7L7F-J|L--7F||||FJFJFJL7|FJL-7L7J||L-7F7L-7LJ||FJF-|LJFJ7LJJL7L--7JF77LLFF7
FLJ.7||..FLJJ.F.L.L-.LL-7F-7L-7L7|LL-J|F7F7LJL--7||LJ||F-J||FJ|F7L7|L-7|F-7|FJ|||L-J-L7FJLJF-7L7L7LJF-J|L--JJ|7F77JL7.F7J--7..F.7-F7F|--FL7-
|.LFJ-7J-JFL.FFJJF--||.L||FJF7|JLJLLF7LJ||L-7F7FJ|L-7|||F7|LJ.LJ|FJL-7|||F||L-J||F----JL-7LL7|||FJF-JF7L---7.FL-|--F|F-LJ7-J.FF-JL-FJJFLF-J|
|F-J|.|FFFJ.-.|..LJ-LF--J|L7||L7JJ-L||F7|L7FJ|||FJF7|LJ|||L-7F--JL7LFJ|LJ-LJL|JLJL-7F-7F7|F7||FJL7L7FJ|F---J-|.|L|.FJLJ|||J---J7JF--7LJ7L|7|
JJLFJF7J7J.L.-L-F|J.FL7F7||||L7|7L|L|LJLJFJ|FJ||L7||L7|LJ|F7|L-7F-JFL7|JLF||F--JJ-FJ|FJ||||LJ|L-7L7||J|L--7J--7|.--L7L--7JF-|.||.|FJL.L|F--.
LLF|LJ.|J|7L..|-FF-|FL||LJ-LJLLJ|FL.|F7F7L7||FJ|.|||FJ7FL||LJF-JL---7LJ-JL-7|..L-F|FJ|FJLJL-7L--JFJLJFJF--JJ.F7.F7LF|-LJL-F7|.|L-J.--7-J-L-7
LL7JJ.F7--L-L-7.|-.F7.LJL|F|.LJJFL.-||LJ|FJ||L-J7|||L7L|||L7FJF-7F7FJ-|.L7JFL77.||LJLLJJ-LF-JF-7FJF||L7|F7|.F7F.LJFL7FF77.FF-7LFJ.|||LFJ.L7.
FF|J.F|J7LL-|FLLLJF7J-||.|-F|-|JLJ7LLJ|LLJ|LJJJ-FLJL-J-L-L-J|FJLLJLJJ-LJ-L7FF-77F7J.|.||.LL-7L7|L--7-L|LJL77.FF--|7||-LL-|-F-J7JF-F77-J.|||J
77L7-LJFLFJ-J77.L7|L--F--J.L.FJF7-FF.|FLLL7JL|J.FJ..||J..L|JLJJ..L||.7||-L|LL7J7|.LF7-L777L|L-JL---JLFJF7FJLF.L7FJL7L-J.F|.|JF|.-7JJJ.LF-F.|
J7J|F|-JJ|J|F--JJLJLJ.L--L7LLJJ7F7|.F-7L--JL-F-JL--FLJ-F-F-JL7|J.F|L7F7F-7|.L|J7-F-|F.LLFJ-|.|LLJL|7.L7||L7FJ7JLF7|JJFL7FJ-|7F-7LJJ.-FJ.L--|
LJ.J-F-.|F-7JFLLF-F77LL7LLJ.|L|7|.7FFJL.LL7JF-J--J7FJF||-J.-7JJ.--|L7.-JLL-L7|L.L||L.|7.L|7.-L7L.7J-LFJ|L7L7.77J.|JJ.|.F7.FL7LL|J||.|..F.FL.
FFJJ7||FJ-7L.7|-LJJ|J.||7J|-7-FJFF7JL-F|..LF7J||..JL7J|JF|.LJ7FFJLL7|-|F7..LL77.7LF77.FF|||-L7L..--|.L7|JL7|F-.F7J||.F-J|-7F-7J|7J7.J--F77.F
-J.FL|JJ|.J|-LJ7||FJJFJ||--7L-|-|LJ7.LLJ77F|J.---7.||LJF|LJFFF7-JLL7|.LJ-777..-7LFLL-7F7J-J--7FF7..L|L|||FLJ--7-|7-LF7.F7.7J|.F||.L.L|.LLJ77
||FL-|L-JFL-.L-FF-7|.F7F77LFJL|JJ|.F.||7.L-|FJL7-7J--7--J.LL-JLL77-||77J.||---J|.J-JF7-|JFL7|||JL-7JJFJ|77-LJ7JLJ.|-J|F|J||JF|-J7|J7..|77..7
FL..F-.J.7J-LJJ|LL-J-LL7JLJLJ..|.F7L7-F|J-LJJJ-L.LLJJ.FJL|...-.FJL-LJJLF7.J.F-J.-|LL-.LFJ.L-F-J.LJJJJL-JJF.JJL-7J-JJLLJJ-JL.LL7LJJL-7-LJJJ-."""

    number_of_steps, track = find_path(maze.split("\n"))
    print("Number of steps: ", number_of_steps)
    print_grid(track)

