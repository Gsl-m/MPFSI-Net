def get_rand_bbox(width, height, l):
    r_x = np.random.randint(width)
    r_y = np.random.randint(height)
    r_l = np.sqrt(1 - l)
    r_w = np.int(width * r_l)
    r_h = np.int(height * r_l)
    bb_x_1 = np.clip(r_x - r_w // 2, 0, width)
    bb_y_1 = np.clip(r_y - r_h // 2, 0, height)
    bb_x_2 = np.clip(r_x + r_w // 2, 0, width)
    bb_y_2 = np.clip(r_y + r_h // 2, 0, height)
    return bb_x_1, bb_y_1, bb_x_2, bb_y_2
