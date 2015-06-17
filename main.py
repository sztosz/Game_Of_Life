import tdl

HEIGHT = 80
WIDTH = 80
FPS = 10

class Game:

    def __init__(self):
        self.console = tdl.init(WIDTH, HEIGHT, "Game of life", fullscreen=False, renderer='SDL')
        self.board = []
        self.is_running = False
        self.step = 0

    def load_board(self, file_name):
        with open(file_name) as f:
            content = f.readlines()
            for y_, line in enumerate(content):
                self.board.append([])
                for x_, char in enumerate(line.strip('\n')):
                    self.board[y_].append(Tile((x_, y_), visibility=(False if char == ' ' else True)))

    def center_and_extend_loaded_board(self):
        pass

    def run(self):
        self.is_running = True
        while self.is_running:
            self.draw()
            self.process_input()
            self.compute()
            self.step += 1

    def draw(self):
        self.console.clear()
        for row in self.board:
            for tile in row:
                tile.draw(self.console)
        tdl.flush()
        tdl.set_title("STEP {0}".format(self.step))

    def process_input(self):
        for event in tdl.event.get():
            if event.type == 'QUIT':
                raise SystemExit()

    def process_input_step_by_step(self):
        loop = True
        while loop:
            event = tdl.event.key_wait()
            if event.type == 'KEYDOWN' and event.alt and event.key == 'F4':
                raise SystemExit
            if event.key == 'SPACE':
                loop = False

    def compute(self):
        for row in self.board:
            for tile in row:
                tile.count_neighbours(self.board)
                tile.set_visibility()


class Tile:

    def __init__(self, coords, sprite='#', visibility=False, colour=(200, 200, 200)):
        self.visibility = visibility
        self.next_step_visibility = visibility
        self.sprite = sprite
        self.colour = colour
        self.x, self.y = coords
        self.neighbours = None  # Just initializing, so my IDE does not bark at me

    def count_neighbours(self, board):
        neighbours = 0
        for x_ in (-1, 0, 1):
            for y_ in (-1, 0, 1):
                if x_ == 0 and y_ == 0:
                    continue  # we don't want to count ourselves
                try:
                    if board[self.y + y_][self.x + x_].visibility:
                        neighbours += 1
                except IndexError:
                    # we don't want error when we are checking border of map
                    X = self.x + x_  # just a debugging help
                    Y = self.y + y_  # just a debugging help
                    # print(X, Y)
        self.neighbours = neighbours
        # print(neighbours)

    def set_visibility(self):
        if not self.visibility:
            if self.neighbours == 3:
                self.next_step_visibility = True
        else:
            if self.neighbours > 3:
                self.next_step_visibility = False
            elif self.neighbours < 2:
                self.next_step_visibility = False

    def draw(self, console):
        self.visibility = self.next_step_visibility
        if self.visibility:
            console.draw_char(self.x, self.y, self.sprite, self.colour)

if __name__ == '__main__':
    tdl.set_fps(FPS)
    game = Game()
    game.load_board('board.txt')
    game.run()
    # print('')
