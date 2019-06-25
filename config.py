# 游戏面板方格数
num_x = 12
num_y = 20
# 方格的宽高
base_square_weight = 20
base_square_height = 20
# 方格间距
gap_square = 3

# 主面板
# x,y,宽,高
gap_edge = 10
main_board_weight: int = num_x * base_square_weight + (num_x + 1) * gap_square
main_board_height: int = num_y * base_square_height + (num_y + 1) * gap_square
main_board_x: int = gap_edge
main_board_y: int = gap_edge
main_board_rect: [int, int, int, int] = [main_board_x, main_board_y, main_board_weight, main_board_height]
# 主面板边框颜色
color_main_board_line: tuple = (0, 0, 0)
# 主面板边框粗细
size_main_board_line: int = 1

score_board_weight: int = int(4/5*main_board_weight)
score_board_height: int = (main_board_height-gap_edge)//2
score_board_x: int = main_board_x+main_board_weight+gap_edge
score_board_y: int = gap_edge
score_board_rect: [int, int, int, int] = [score_board_x, score_board_y, score_board_weight, score_board_height]
# 主面板边框颜色
color_score_board_line: tuple = (0, 0, 0)
# 主面板边框粗细
size_score_board_line: int = 1


# 游戏性相关
# 游戏速度 毫秒 越低越快
cycle = 500
level = [1 + 0.1 * x for x in range(11)]
# 主窗口
# 窗口宽度
main_weight: int = main_board_weight+score_board_weight+3*gap_edge
# 窗口高度
main_height: int = main_board_height + 2 * gap_edge
# 窗口背景
color_bg = (255, 255, 255)

next_board_weight: int = int(4/5*main_board_weight)
next_board_height: int = main_height-score_board_height-3*gap_edge
next_board_x: int = main_board_x+main_board_weight+gap_edge
next_board_y: int = score_board_y+score_board_height+gap_edge
next_board_rect: [int, int, int, int] = [next_board_x, next_board_y, next_board_weight, next_board_height]
# 主面板边框颜色
color_next_board_line: tuple = (0, 0, 0)
# 主面板边框粗细
size_next_board_line: int = 1