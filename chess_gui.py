import chess_engine
import ai_engine
from enums import Player
import logging
import pygame as py

logging.basicConfig(filename='chess_game.log', format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
"""Variables"""
WIDTH = HEIGHT = 512  # width and height of the chess board
DIMENSION = 8  # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the chess pieces

colors = [py.Color("white"), py.Color("gray")]  # colors for the board

py.display.set_caption("Chess")
icon = py.image.load("images/chess_icon.png")
py.display.set_icon(icon)


# Done
def load_images():
    """
    load the images and there size and save in global dict - IMAGES
    """
    for p in Player.PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))


# Done
def draw_squares(screen):
    """ Draw the chess board with the alternating two colors

    :param screen: the pygame screen
    """
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]  # color = (row + col) % 2 == 0 ? white : gray
            # draw on the screen a rectangle with the above color
            rect = py.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            py.draw.rect(screen, color, rect)


# Done
def draw_pieces(screen, game_state):
    """ Draw the chess pieces onto the board

    :param screen:          -- the pygame screen
    :param game_state:      -- the current state of the chess game
    """
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = game_state.get_piece(row, col)
            if piece is not None and piece != Player.EMPTY:
                rect = py.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                screen.blit(IMAGES[piece.get_player() + "_" + piece.get_name()], rect)


# Done
def draw_game_state(screen, game_state, valid_moves, square_selected):
    """ Draw the complete chess board with pieces

    Keyword arguments:
        :param screen       -- the pygame screen
        :param game_state   -- the state of the current chess game
    """
    draw_squares(screen)
    highlight_square(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state)


# Done
def draw_text(screen, text):
    font = py.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, False, py.Color("Black"))
    text_location = py.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                      HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)


# Done
def highlight_square(screen, game_state, valid_moves, square_selected):
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
        row = square_selected[0]
        col = square_selected[1]

        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_1)) or \
                (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_2)):
            # hightlight selected square
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(py.Color("blue"))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

            # highlight move squares
            s.fill(py.Color("green"))

            for move in valid_moves:
                screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))


def main():
    # Check for the number of players and the color of the AI
    human_player = ""
    # set players methods
    while True:
        try:
            number_of_players = input("How many players (1 or 2)?\n")
            if int(number_of_players) == 1:
                number_of_players = 1
                while True:
                    human_player = input("What color do you want to play (w or b)?\n")
                    if human_player == "w" or human_player == "b":
                        break
                    else:
                        print("Enter w or b.\n")
                break
            elif int(number_of_players) == 2:
                number_of_players = 2
                break
            else:
                print("Enter 1 or 2.\n")
        except ValueError:
            print("Enter 1 or 2.")

    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    load_images()
    running = True
    square_selected = ()  # keeps track of the last selected square
    player_clicks = []  # keeps track of player clicks (two tuples)
    valid_moves = []
    game_over = False
    ai = ai_engine.chess_ai()
    game_state = chess_engine.game_state()

    if human_player == 'b':
        logging.info("AI player start")
        ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
        game_state.move_piece(ai_move[0], ai_move[1], True)
    elif human_player == "w":
        logging.info("Human player start")
    else:
        logging.info("White player start")

    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
                if not game_over:
                    location = py.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if square_selected == (row, col):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2:
                        if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []
                        else:
                            game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
                                                  (player_clicks[1][0], player_clicks[1][1]), False)

                            draw_game_state(screen, game_state, valid_moves, square_selected)
                            py.display.update()
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []
                            if human_player == 'w':
                                ai_move = ai.minimax_white(game_state, 3, -100000, 100000, True, Player.PLAYER_2)
                                try:
                                    game_state.move_piece(ai_move[0], ai_move[1], True)
                                except:
                                    running = False

                            elif human_player == 'b':
                                ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
                                try:
                                    game_state.move_piece(ai_move[0], ai_move[1], True)
                                except:
                                    running = False
                    else:
                        valid_moves = game_state.get_valid_moves((row, col))
                        if valid_moves is None:
                            valid_moves = []
            elif e.type == py.KEYDOWN:
                if e.key == py.K_r:
                    game_over = False
                    game_state = chess_engine.game_state()
                    square_selected = ()
                    player_clicks = []
                    valid_moves = []
                elif e.key == py.K_u:
                    game_state.undo_move()
                    print(len(game_state.move_log))

        draw_game_state(screen, game_state, valid_moves, square_selected)
        endgame = game_state.checkmate_stalemate_checker()
        if endgame in (0, 1, 2):
            if endgame == 0:
                draw_text(screen, "Black wins.")
                logging.info("Black wins.")
            elif endgame == 1:
                draw_text(screen, "White wins.")
                logging.info("White wins.")
            elif endgame == 2:
                draw_text(screen, "Stalemate.")
                logging.info("Stalemate.")
            game_over = True
            running = False

            py.display.update()
            py.time.wait(1000)
        clock.tick(MAX_FPS)
        py.display.flip()

    # LOGGING PART
    check_counter_white = sum(1 for i in range(0, len(game_state.move_log), 2) if game_state.move_log[i].in_check)
    check_counter_black = sum(1 for i in range(1, len(game_state.move_log), 2) if game_state.move_log[i].in_check)
    logging.info(f"Number of chess on the white {check_counter_white}")
    logging.info(f"Number of chess on the black {check_counter_black}")

    first_index_white = first_index_black = len(game_state.move_log) + 1
    # The first white removed piece
    for index in range(1, len(game_state.move_log), 2):
        if game_state.move_log[index].removed_piece != Player.EMPTY and \
                game_state.move_log[index].removed_piece is not None:
            first_index_white = index
            break
    # The first black removed piece
    for index in range(0, len(game_state.move_log), 2):
        if game_state.move_log[index].removed_piece != Player.EMPTY and \
                game_state.move_log[index].removed_piece is not None:
            first_index_black = index
            break

    logging.info(f"All of White's pieces survived {first_index_white} turns")
    logging.info(f"All of Black's pieces survived {first_index_black} turns\n")
    py.quit()


if __name__ == "__main__":
    main()
