import enums.constants as const

color = ( 0, 0, 0)

values = []



# top and bottom sections
values.extend([[i, j] for j in range(const.BORDER_WIDTH + const.TITLE_HEIGHT) for i in range(const.WIDTH_IN_CELLS)])
values.extend([i, const.HEIGHT_IN_CELLS - (j)] for j in range(const.BORDER_WIDTH + 1) for i in range(const.WIDTH_IN_CELLS))

# left and right section
values.extend([j, i] for j in range(const.BORDER_WIDTH) for i in range(const.BORDER_WIDTH, const.HEIGHT_IN_CELLS - const.BORDER_WIDTH))
values.extend([const.WIDTH_IN_CELLS - const.BORDER_WIDTH + j, i] for j in range(const.BORDER_WIDTH + 1) for i in range(const.BORDER_WIDTH, const.HEIGHT_IN_CELLS - const.BORDER_WIDTH))