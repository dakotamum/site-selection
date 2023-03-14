import enums.constants as const

color = ( 0, 0, 0)

values = []

# top and bottom sections
values.extend([[i, j] for j in range(5) for i in range(const.WIDTH_IN_CELLS)])
values.extend([i, const.HEIGHT_IN_CELLS - 3 + j] for j in range(3) for i in range(const.WIDTH_IN_CELLS))

# left and right sections
values.extend([j, i] for j in range(3) for i in range(3, const.HEIGHT_IN_CELLS - 3))
values.extend([const.WIDTH_IN_CELLS - 3 + j, i] for j in range(3) for i in range(3, const.HEIGHT_IN_CELLS - 3))