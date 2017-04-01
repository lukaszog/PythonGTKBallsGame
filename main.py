# coding=utf-8
from random import randrange

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf


class Cell(Gtk.Button):
    def __init__(self):
        Gtk.Button.__init__(self)
        self.ball_color = None
        self.is_ball = None
        self.button = Gtk.ToggleButton().new()
        self.button.set_size_request(50, 50)

    def place_ball(self, color):

        ball = GdkPixbuf.Pixbuf.new_from_file_at_size(str(color) + '.svg', 35, 35)
        image = Gtk.Image()
        image.set_from_pixbuf(ball)
        self.button.add(image)
        self.ball_color = color
        self.is_ball = True


class BallsGrid(Gtk.Grid):
    def __init__(self, rows, cols):
        Gtk.Grid.__init__(self)
        self.rows = rows
        self.cols = cols
        self.cells = []

        for row in range(rows):
            for col in range(cols):
                cell = Cell()
                self.cells.append(cell)
                self.attach(cell.button, row, col, 1, 1)

        self.place_balls()

    def place_balls(self):

        balls = 0
        dict = {1: 'blue', 2: 'fiolet', 3: 'green', 4: 'red', 5: 'yellow'}

        while balls <= 50:

            row = randrange(0, self.rows)
            col = randrange(0, self.cols)
            color = randrange(1, 6)

            i = self.get_index(row, col)

            self.cells[i].place_ball(dict[color])
            balls += 1

    def get_row_col_button(self, index):
        return index / self.cols, index % self.cols

    def get_index(self, row, col):
        """Funkcja zwraca index na podstawie wiersza i kolumny"""
        return (row * self.cols) + col


class App(Gtk.Window):
    """Główna klasa rozruchowa, inicjuje widok aplikacji"""
    def __init__(self, rows, cols):
        Gtk.Window.__init__(self)
        self.grid = BallsGrid(rows, cols)
        self.window = Gtk.Window()
        self.rows = rows
        self.cols = cols
        self.clicked = 0
        self.first_click = -1
        self.second_click = -1
        self.vbox = Gtk.VBox()
        self.window.add(self.vbox)
        self.create_grid()
        self.window.connect('destroy', Gtk.main_quit)

    def create_grid(self):
        # tworzenie poszczególnych połączeń do przycisków
        for i, cell in enumerate(self.grid.cells):
            (row, col) = self.grid.get_row_col_button(i)
            cell.button.connect('clicked', self.clicked_handler, row, col)

        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.vbox.pack_start(self.grid, expand=True, fill=True, padding=0)

    def clicked_handler(self, button, row, col):

        index = self.grid.get_index(row, col)

        if button.get_active():
            if self.first_click == -1:
                self.first_click = index
            else:
                print 'Drugie klikniecie'
                self.second_click = index

            if self.first_click != -1 and self.second_click != -1:
                print 'Mamy dwa klikniecia'
                self.grid.cells[self.first_click].button.set_active(False)
                self.grid.cells[self.second_click].button.set_active(False)
                self.first_click, self.second_click = -1, -1

            self.clicked += 1
        else:
            self.grid.cells[index].button.set_active(False)

        if self.clicked == 2:
            print '2 buttony'
            self.clicked = 0

            #self.grid.cells[self.first_click].button.set_active(False)

        print 'Wiersz {} kolumna {}'.format(row, col)


if __name__ == "__main__":
    win = App(10, 10)
    win.window.show_all()
    Gtk.main()
