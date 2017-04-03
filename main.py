# coding=utf-8
from random import randrange

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf


class Cell(Gtk.Button):
    def __init__(self):
        Gtk.Button.__init__(self)
        self.ball_color = None
        self.is_ball = False
        self.button = Gtk.ToggleButton().new()
        self.button.set_size_request(50, 50)

    def place_ball(self, color):

        ball = GdkPixbuf.Pixbuf.new_from_file_at_size(str(color) + '.svg', 35, 35)
        image = Gtk.Image()

        image.set_from_pixbuf(ball)
        image.show()
        self.ball_color = color
        self.is_ball = True
        self.button.add(image)
        self.button.show()

# noinspection PyUnresolvedReferences
class BallsGrid(Gtk.Grid):
    def __init__(self, rows, cols):
        Gtk.Grid.__init__(self)
        self.rows = rows
        self.cols = cols
        self.cells = []
        self.dict = {1: 'blue', 2: 'fiolet', 3: 'green', 4: 'red', 5: 'yellow'}

        for row in range(rows):
            for col in range(cols):
                cell = Cell()
                self.cells.append(cell)
                self.attach(cell.button, row, col, 1, 1)

        self.place_balls(5)

    def place_balls(self, number):

        balls = 0

        while balls <= number:

            row = randrange(0, self.rows)
            col = randrange(0, self.cols)
            color = randrange(1, 6)

            i = self.get_index(row, col)

            if not self.cells[i].is_ball:
                self.cells[i].place_ball(self.dict[color])
                balls += 1

    def move_ball(self, from_point, to_point):

        color = self.cells[from_point].ball_color
        self.cells[to_point].place_ball(color)
        print self.cells[to_point]
        self.cells[from_point].button.get_child().destroy()
        self.cells[from_point].is_ball = False
        self.place_balls(3)

        (row, col) = self.get_row_col_button(to_point)

        # szukam sasiada

        index_horizontal_right = self.get_index(row + 1, col)
        index_horizontal_left = self.get_index(row - 1, col)

        index_vertical_up = self.get_index(row, col + 1)
        index_vertical_down = self.get_index(row, col - 1)

        horizontal_left, horizontal_right = 0, 0
        vertical_top, vertival_down = 0, 0

        if self.cells[index_horizontal_left].ball_color == color:
            horizontal_left += 1
        if self.cells[index_horizontal_right].ball_color == color:
            horizontal_right += 1
        if self.cells[index_vertical_up].ball_color == color:
            vertical_top += 1
        if self.cells[index_vertical_down].ball_color == color:
            vertival_down += 1

        for i in range(0, 5):

            if index_horizontal_left <= 90:
                if self.cells[index_horizontal_left].ball_color == color:
                    horizontal_left += 1
            if index_horizontal_right <= 90:
                if self.cells[index_horizontal_right].ball_color == color:
                    horizontal_right += 1
            if index_vertical_up <= 90:
                if self.cells[index_vertical_up].ball_color == color:
                    vertical_top += 1
            if index_horizontal_right <= 90:
                if self.cells[index_vertical_down].ball_color == color:
                    vertival_down += 1

            index_vertical_up += 1
            index_vertical_down -= 1
            index_horizontal_left -= 10
            index_horizontal_right += 10

        if horizontal_left == 5:
            for i in range(0, 5):
               delete_point = self.get_index(row - i, col)
               self.cells[delete_point].button.get_child().destroy()

        if horizontal_right == 5:
            for i in range(0, 5):
               delete_point = self.get_index(row + i, col)
               self.cells[delete_point].button.get_child().destroy()

        if vertical_top == 5:
            for i in range(0, 5):
                delete_point = self.get_index(row, col + i)
                self.cells[delete_point].button.get_child().destroy()

        if vertival_down == 5:
            for i in range(0, 5):
                delete_point = self.get_index(row, col - i)
                self.cells[delete_point].button.get_child().destroy()

    def get_row_col_button(self, index):
        return index / self.cols, index % self.cols

    def get_index(self, row, col):
        return (row * self.cols) + col


class App(Gtk.Window):
    def __init__(self, rows, cols):
        Gtk.Window.__init__(self)
        self.grid = BallsGrid(rows, cols)
        self.rows = rows
        self.cols = cols
        self.click_count = 0
        self.clicked = 0
        self.first_click = -1
        self.second_click = -1
        self.vbox = Gtk.Box()
        self.main_box = Gtk.VBox()
        self.ptk = Gtk.Box()
        self.point_box = Gtk.Box(spacing=2)

        self.ranking_box = Gtk.Grid()

        self.ranking_label = Gtk.Label(label="Ranking:")
        self.ranking_label.set_margin_right(2)
        self.label1 = Gtk.Label(label="1 ")
        self.label2 = Gtk.Label(label="2 ")

        self.ranking_box.attach(self.ranking_label, 0, 0, 1, 1)
        self.ranking_box.attach(self.label1, 0, 1, 11, 1)
        self.ranking_box.attach(self.label2, 0, 2, 1, 1)

        self.point_label = Gtk.Label(label="Liczba punktow:")
        self.point_label_score = Gtk.Label(label="22")

        self.point_label.set_alignment(0, 0.5)
        self.point_label_score.set_alignment(-501, 220)

        self.point_box.add(self.point_label)
        self.point_box.add(self.point_label_score)

        self.vbox.add(self.ranking_box)
        self.main_box.add(self.point_box)
        self.main_box.add(self.vbox)
        self.add(self.main_box)

        self.create_grid()

        self.connect('destroy', Gtk.main_quit)




    def create_grid(self):
        # tworzenie poszczególnych połączeń do przycisków

        for i, cell in enumerate(self.grid.cells):
            (row, col) = self.grid.get_row_col_button(i)
            cell.button.connect('clicked', self.clicked_handler, row, col)

        button = Gtk.Button("Nowa gra")
        button.connect('clicked', lambda x: self.restart())
        self.main_box.add(button)

        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.vbox.pack_start(self.grid, expand=False, fill=True, padding=0)

    def restart(self):
        """FUnkcja odpowiedzialna za restart gry"""
        self.destroy()
        self.vbox.remove(self.grid)
        self.create_grid()
        self.window.show_all()

    def clicked_handler(self, button, row, col):

        index = self.grid.get_index(row, col)

        if button.get_active():
            if self.first_click == -1:
                self.first_click = index
            else:
                self.second_click = index

            if self.first_click != -1 and self.second_click != -1:
                self.clicked = 0

                from_point = self.first_click
                to_point = self.second_click

                if self.grid.cells[from_point].is_ball:
                    self.grid.move_ball(from_point, to_point)
                    self.click_count += 1

                self.grid.cells[self.first_click].button.set_active(False)
                self.grid.cells[self.second_click].button.set_active(False)
                self.first_click, self.second_click = -1, -1

            self.clicked += 1
        else:
            self.grid.cells[index].button.set_active(False)


if __name__ == "__main__":
    win = App(10, 10)
    win.show_all()
    Gtk.main()
