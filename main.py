# coding=utf-8
from random import randrange

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

# liczba kulek przy starcie gry
BALLS_AMOUNT = 50
# liczba nowych kulek po przestawieniu kuli
BALLS_PER_CLICK = 3

# liczba kolumn
SIZE_X = 10
# liczba wierszy
SIZE_Y = 10

"""Prosta gra w kulki z wykorzystaniem GTK 3."""


class Cell(Gtk.Button):
    """Klasa reprezentuje pojedynczą komórkę na planszy.
    
    Klasa dziedziczy po Gtk.Button.
    """
    def __init__(self):
        """Każda komórka ma ustawione: ball_color - informuje o kolorze kulki ustawionej na polu.
        
        is_ball - informuje czy na polu znajduje sie kulka.
        
        button - tworzy nowy przycisk, nastepnie są ustawiane wymiary przycisku.
        """
        Gtk.Button.__init__(self)
        self.ball_color = None
        self.is_ball = False
        self.button = Gtk.ToggleButton().new()
        self.button.set_size_request(50, 50)
        self.button.show()

    def place_ball(self, color):
        """Funkcja odpowiedzialna za wstawienie do komórki obrazka."""
        ball = GdkPixbuf.Pixbuf.new_from_file_at_size(str(color) + '.svg', 35, 35)
        image = Gtk.Image()
        image.set_from_pixbuf(ball)
        image.show()
        # ustawienie koloru na pole
        self.ball_color = color
        self.is_ball = True
        # dodanie obrazka do przycisku
        self.button.add(image)
        self.button.show()


class BallsGrid(Gtk.Grid):
    """Klasa odpowiedzialna za narysowanie planszy do gry."""
    def __init__(self, rows, cols):
        """Konstruktor przyjmuje ilosc wierszy - rows obraz ilosc kolumn - cols."""
        Gtk.Grid.__init__(self)
        self.rows = rows
        self.cols = cols
        # lista komórek
        self.cells = []
        # słownik do kolorów kulek
        self.dict = {1: 'kulka1', 2: 'kulka2', 3: 'kulka3', 4: 'kulka4', 5: 'kulka5'}

        # ustawianie przyciskow na planszy
        for row in range(rows):
            for col in range(cols):
                cell = Cell()
                cell.show()
                self.cells.append(cell)
                self.attach(cell.button, row, col, 1, 1)
        # generowanie liczby kulek
        self.place_balls(BALLS_AMOUNT)

    def place_balls(self, number):
        """Funckja ustawia na planszy określoną przez argument number liczbę kulek nba planszy."""
        balls = 0
        while balls <= number:

            row = randrange(0, self.rows)
            col = randrange(0, self.cols)
            color = randrange(1, 6)
            print color
            i = self.get_index(row, col)
            # jeżeli wybrane pole nie zawiera kulki ustawiamy ją
            if not self.cells[i].is_ball:
                self.cells[i].place_ball(self.dict[color])
                balls += 1

    def check_balls(self):
        """Funkcja odpowiedzialna za sprawdzenie czy znajduje się 5.
                
        takich samych kulek kolejno w poziomie, pionie, po skosach.
        """

        # iteracja dla kazdego pola
        for row in range(self.rows):
            for col in range(self.cols):

                index = self.get_index(row, col)

                # jezeli pole posiada kulke sprawdzamy...
                if self.cells[index].is_ball:
                    # liczniki dla poszczegolnych orientacji
                    vertical, horizontal, cross, cross_up = 0, 0, 0, 0
                    # kolor napotkaniej kulki
                    color = self.cells[index].ball_color
                    coor, coor_horizontal, coor_cross, coor_cross_up = index, index, index, index
                    # tworzenie list służących do zapisywania pol, w ktorych znajduja sie kulki
                    delete_vertical, delete_horizontal, delete_cross, delete_cross_up = [], [], [], []
                    # petla sprawdza i zlicza wystapienia kulek obok siebie w tym samym kolorze
                    # w poziomie, w pionie, po skosie w prawo, po skosie w lewo
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
                        # zwiekszamy zmienna dla poszukiwania kulek po skosie w lewo
                        coor_cross_up += 9
                        # zwiekszamy zmienna dla poszukiwania kulek po skosie w prawo
                        coor_cross += 11
                        # zwiekszamy zmienna dla poszukiwania kulek poziomo
                        coor_horizontal += 10
                        # zwiekszamy zmienna dla poszukiwania kulek pionowo
                        coor += 1

                    # jezeli petla znajdzie 5 kulek w okreslonej orientacji usuwamy je
                    if vertical == 5:
                        for i, val in enumerate(delete_vertical):
                            self.cells[val].is_ball = False
                            self.cells[val].ball_color = None
                            self.cells[val].button.get_child().destroy()

                    if horizontal == 5:
                        for i, val in enumerate(delete_horizontal):
                            self.cells[val].is_ball = False
                            self.cells[val].ball_color = None
                            self.cells[val].button.get_child().destroy()

                    if cross == 5:
                        for i, val in enumerate(delete_cross):
                            self.cells[val].is_ball = False
                            self.cells[val].ball_color = None
                            self.cells[val].button.get_child().destroy()

                    if cross_up == 5:
                        for i, val in enumerate(delete_cross_up):
                            self.cells[val].is_ball = False
                            self.cells[val].ball_color = None
                            self.cells[val].button.get_child().destroy()

    def get_index(self, row, col):
        """Funkcja zwraca numer odpowiadajacy indeksowy w tablicy komorek.
        
        Funkcja przyjmuje wiersz - row i kolumne - col danego pola.
        """
        return (row * self.cols) + col

    def ball_num(self):
        """Funkcja zwraca liczbe kulek aktualnie na planszy."""
        counter = 0
        for i in range(0, 100):
            if self.cells[i].is_ball:
                counter += 1
        return int(counter)


class App(Gtk.Window):
    """Główna klasa rozruchowa aplikacji."""
    def __init__(self, rows, cols):
        """Klasa odpowiedzialna za widok aplikacji i obsługę ruchów."""
        Gtk.Window.__init__(self)
        self.set_title("Kulki")
        # stworzenie siatki pol
        self.grid = BallsGrid(rows, cols)
        self.rows = rows
        self.cols = cols
        # w tej tablicy przechowujemy wyniki
        self.points_arr = []
        # licznik klikniec
        self.click_count = 0
        self.clicked = 0
        self.balls_num = 0
        self.first_click = -1
        self.second_click = -1
        # box dla siatki z polami
        self.vbox = Gtk.Box()
        # główny box do którego wszystko jest zamykane
        self.main_box = Gtk.VBox()
        # box w ktorym przechowywana jest aktualna lista punktów
        self.point_box = Gtk.Box(spacing=2)
        # box dla listy rankingowej
        self.ranking_box = Gtk.Grid()
        self.ranking_label = Gtk.Label()
        self.vbox.add(self.ranking_box)
        self.main_box.add(self.point_box)
        self.main_box.add(self.vbox)
        self.add(self.main_box)
        self.ranking_panel()
        # listenerow na polach
        self.create_grid()
        self.point_label = Gtk.Label(label="Liczba punktow:")
        self.point_label_score = Gtk.Label()
        self.point_label_score.set_markup("<b>0</b>")
        self.point_label.set_alignment(0, 0.5)
        self.point_box.add(self.point_label)
        self.point_box.add(self.point_label_score)
        self.connect('destroy', Gtk.main_quit)

    def ranking_panel(self):
        """Funkcja odpowiedzialna za wyswietlenie listy rankingowej."""
        self.ranking_label.set_markup("<b>Ranking: </b>")
        self.ranking_label.set_margin_right(2)
        self.points_arr.sort(reverse=True)
        for i, val in enumerate(self.points_arr):
            scode_label = Gtk.Label()
            lp = i + 1
            if i < 5:
                scode_label.set_markup("<b>" + str(lp) + ".</b> " + str(val))
                self.ranking_box.attach(scode_label, 0, i + 2, 1, 1)

        self.ranking_box.attach(self.ranking_label, 0, 0, 1, 1)
        self.ranking_box.show_all()
        self.ranking_label.show_all()

    def create_grid(self):
        """Funckja odpowiedzialna za utworzenie poszczególnych połączeń do przycisków."""
        # tworzenie poszczególnych połączeń do przycisków
        for i, cell in enumerate(self.grid.cells):
            (row, col) = i / self.cols, i % self.cols
            cell.button.connect('clicked', self.clicked_handler, row, col)

        button = Gtk.Button("Graj od początku")
        button.connect('clicked', lambda x: self.restart())
        self.main_box.add(button)

        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.vbox.pack_start(self.grid, expand=False, fill=True, padding=0)

    def restart(self):
        """FUnkcja odpowiedzialna za restart gry."""
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
        """Obsługa kliknięć i przenoszeń kul."""
        index = self.grid.get_index(row, col)
        if button.get_active():
            if self.first_click == -1:
                self.first_click = index
            else:
                self.second_click = index
            # jezeli dokonamy dwoch klikniec przechodzimy do przesuniecia kuli
            if self.first_click != -1 and self.second_click != -1:
                self.clicked = 0

                from_point = self.first_click
                to_point = self.second_click

                # jezeli drugie pole jest niepuste dokonujemy przesuniecia
                if self.grid.cells[from_point].is_ball and self.first_click != self.second_click \
                        and self.grid.cells[from_point].is_ball != self.grid.cells[to_point].is_ball:
                    # przesuwamy kule
                    self.move_ball(from_point, to_point)
                    # zwiekszamy licznik klikniec
                    self.click_count += 1
                    self.point_label_score.set_markup("<b>" + str(self.click_count) + "</b>")
                    self.point_label_score.show_all()

                # zwolnienie przycisku
                self.grid.cells[self.first_click].button.set_active(False)
                self.grid.cells[self.second_click].button.set_active(False)
                self.first_click, self.second_click = -1, -1

            self.clicked += 1
        else:
            self.grid.cells[index].button.set_active(False)

    def move_ball(self, from_point, to_point):
        """Funckja odpowiedzialna za przestawienie kuli."""
        color = self.grid.cells[from_point].ball_color
        self.grid.cells[to_point].place_ball(color)
        self.grid.cells[from_point].button.get_child().destroy()
        self.grid.cells[from_point].is_ball = False
        self.grid.cells[from_point].ball_color = None
        # sprawdzamy czy jest 5 kul w danej orientacji
        self.grid.check_balls()
        # sprawdzamy czy uzytkownik nie zapelnił całej planszy
        self.if_player_lose()
        # losujemy i ustawiamy kolejne kule
        self.grid.place_balls(BALLS_PER_CLICK)
        # sprawdzamy czy jest 5 kul w danej orientacji
        self.grid.check_balls()

    def if_player_lose(self):
        """W przypadku zapełnienia planszy kulkami, wyswietlamy komunikat i restartujemy gre."""
        if self.grid.ball_num() == 99:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "Przegrałeś")
            dialog.format_secondary_text(
                "Zagraj jeszcze raz")
            dialog.run()
            dialog.destroy()
            self.restart()

if __name__ == "__main__":
    win = App(SIZE_X, SIZE_Y)
    win.show_all()
    Gtk.main()
