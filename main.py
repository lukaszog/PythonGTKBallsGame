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
        self.button.show()

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
        self.dict = {1: 'kulka1', 2: 'kulka2', 3: 'kulka3', 4: 'kulka4', 5: 'kulka5'}

        for row in range(rows):
            for col in range(cols):
                cell = Cell()
                cell.show()
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
        self.cells[from_point].button.get_child().destroy()
        self.cells[from_point].is_ball = False
        self.cells[from_point].ball_color = None
        self.place_balls(3)
        self.check_balls()

    def check_balls(self):

        for row in range(self.rows):
            for col in range(self.cols):
                # szukam sasiada
                index = self.get_index(row, col)

                if self.cells[index].is_ball:
                    vertical, horizontal, cross, cross_up = 0, 0, 0, 0
                    color = self.cells[index].ball_color
                    coor, coor_horizontal, coor_cross, coor_cross_up = index, index, index, index
                    delete_vertical = []
                    delete_horizontal = []
                    delete_cross = []
                    delete_cross_up = []
                    for i in range(0, 5):
                        if coor <= 99:
                            if self.cells[coor].ball_color == color and vertical <= 5:
                                vertical += 1
                                delete_vertical.append(coor)
                        if coor_horizontal <= 99:
                            if self.cells[coor_horizontal].ball_color == color and horizontal <= 5:
                                horizontal += 1
                                delete_horizontal.append(coor_horizontal)
                        if coor_cross <= 99:
                            if self.cells[coor_cross].ball_color == color and cross <= 5:
                                cross += 1
                                delete_cross.append(coor_cross)
                        if coor_cross_up <= 99:
                            if self.cells[coor_cross_up].ball_color == color and cross_up <= 5:
                                cross_up += 1
                                delete_cross_up.append(coor_cross_up)
                        coor_cross_up += 9
                        coor_cross += 11
                        coor_horizontal += 10
                        coor += 1

                    if vertical == 5:
                        print "Mam pionowo kolor {}: ".format(color)
                        for i, val in enumerate(delete_vertical):
                            print 'Usuwam index {} wartosc is_ball {}'.format(val, self.cells[val].is_ball)
                            self.cells[val].is_ball = False
                            self.cells[val].ball_color = None
                            self.cells[val].button.get_child().destroy()

                    if horizontal == 5:
                        for i, val in enumerate(delete_horizontal):
                            print 'Usuwam index {} wartosc is_ball {}'.format(val, self.cells[val].is_ball)
                            self.cells[val].is_ball = False
                            self.cells[val].ball_color = None
                            self.cells[val].button.get_child().destroy()

                    if cross == 5:
                        for i, val in enumerate(delete_cross):
                            print 'Usuwam index {} wartosc is_ball {}'.format(val, self.cells[val].is_ball)
                            self.cells[val].is_ball = False
                            self.cells[val].ball_color = None
                            self.cells[val].button.get_child().destroy()

                    if cross_up == 5:
                        for i, val in enumerate(delete_cross_up):
                            print 'Usuwam index {} wartosc is_ball {}'.format(val, self.cells[val].is_ball)
                            self.cells[val].is_ball = False
                            self.cells[val].ball_color = None
                            self.cells[val].button.get_child().destroy()

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
        self.points_arr = []
        self.click_count = 0
        self.clicked = 0
        self.first_click = -1
        self.second_click = -1
        self.vbox = Gtk.Box()
        self.main_box = Gtk.VBox()
        self.ptk = Gtk.Box()
        self.point_box = Gtk.Box(spacing=2)
        self.ranking_box = Gtk.Grid()
        self.ranking_label = Gtk.Label()
        self.vbox.add(self.ranking_box)
        self.main_box.add(self.point_box)
        self.main_box.add(self.vbox)
        self.add(self.main_box)
        self.ranking_panel()
        self.create_grid()
        self.point_label = Gtk.Label(label="Liczba punktow:")
        self.point_label_score = Gtk.Label()
        self.point_label_score.set_markup("<b>0</b>")
        self.point_label.set_alignment(0, 0.5)
        self.point_box.add(self.point_label)
        self.point_box.add(self.point_label_score)
        self.connect('destroy', Gtk.main_quit)

    def ranking_panel(self):

        self.ranking_label.set_markup("<b>Ranking: </b>")
        self.ranking_label.set_margin_right(2)
        self.points_arr.sort(reverse=True)
        for i, val in enumerate(self.points_arr):
            scode_label = Gtk.Label()
            lp = i + 1
            print "{} {}".format(lp, val)
            scode_label.set_markup("<b>" + str(lp) + ".</b> " + str(val))
            self.ranking_box.attach(scode_label, 0, i + 2, 1, 1)

        self.ranking_box.attach(self.ranking_label, 0, 0, 1, 1)
        self.ranking_box.show_all()
        self.ranking_label.show_all()
        print 'Robie ranking'

    def create_grid(self):
        # tworzenie poszczególnych połączeń do przycisków
        for i, cell in enumerate(self.grid.cells):
            (row, col) = self.grid.get_row_col_button(i)
            cell.button.connect('clicked', self.clicked_handler, row, col)

        button = Gtk.Button("Graj od początku")
        button.connect('clicked', lambda x: self.restart())
        self.main_box.add(button)

        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.vbox.pack_start(self.grid, expand=False, fill=True, padding=0)

    def restart(self):
        """FUnkcja odpowiedzialna za restart gry"""
        self.points_arr.append(self.click_count)
        self.grid.destroy()
        self.click_count = 0
        self.ranking_label.destroy()
        self.ranking_box.destroy()
        self.ranking_box = Gtk.Grid()
        self.vbox.add(self.ranking_box)
        self.ranking_panel()
        self.point_label_score.set_markup("<b>0</b>")
        self.point_label_score.show_all()
        self.grid = BallsGrid(self.rows, self.cols)
        self.create_grid()
        self.grid.show()

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

                if self.grid.cells[from_point].is_ball and self.first_click != self.second_click \
                        and self.grid.cells[from_point].is_ball != self.grid.cells[to_point].is_ball:
                    self.grid.move_ball(from_point, to_point)
                    self.click_count += 1
                    self.point_label_score.set_markup("<b>" + str(self.click_count) + "</b>")
                    self.point_label_score.show_all()

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
