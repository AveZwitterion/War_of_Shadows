from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
import random
import copy


class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical")
        self.seq = ["Bear.png", "Eagle.png", "Elephant.png", "Horse.png", "Lion.png"]
        self.players = [[""] * 5 for _ in range(4)]
        self.positions = ["x 4", "x 3", "x 2", "x 0", "x -1"]
        self.razresh = [[] for _ in range(5)]
        self.cnt = 0
        self.pl_count = 0

        self.label = Label(text="Выберите количество игроков", font_size= 40)
        self.layout.add_widget(self.label)

        for num in range(2, 5):
            btn = Button(text=f"{num} Игрока", font_size= 40)
            btn.bind(on_press=self.button_press)
            self.layout.add_widget(btn)

        self.next_button = Button(text=f"Следующий игрок получил", font_size= 60, on_press=self.show_player_combination)
        return self.layout

    def button_press(self, instance):
        self.pl_count = int(instance.text[0])
        self.generate()
        self.cnt = 0
        self.show_pass_screen()

    def show_pass_screen(self, *_):
        if self.cnt < self.pl_count:
            self.layout.clear_widgets()
            self.label.text = "Передай следующему игроку и нажми кнопку"
            self.layout.add_widget(self.label)
            self.layout.add_widget(self.next_button)
        else:
            self.show_end_screen()

    def show_player_combination(self, *_):
        if self.cnt < self.pl_count:
            self.layout.clear_widgets()
            self.layout.add_widget(Label(text=f"Игрок {self.cnt + 1}:", font_size= 60))
            
            image_layout = BoxLayout(orientation="horizontal")
            text_layout = BoxLayout(orientation="horizontal")


            for i in range(5):
                image_layout.add_widget(Image(source=self.players[self.cnt][i]))
                text_layout.add_widget(Label(text= self.positions[i], font_size= 60))



            #for img_path in self.players[self.cnt]:
            #    image_layout.add_widget(Image(source=img_path))
            #   text_layout.add_widget(Label(text= self.positions[], font_size= 60))
                
            self.layout.add_widget(image_layout)
            self.layout.add_widget(text_layout)
            #self.layout.add_widget(Label(text="x 4     x 3     x 2     x 0    x -1", font_size= 100))
            self.cnt += 1
            hide_button = Button(text="Готов, передаю!", font_size= 60, on_press=self.show_pass_screen)
            self.layout.add_widget(hide_button)
        else:
            self.show_end_screen()

    def show_end_screen(self):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text="Удачной игры!!!", font_size=60))

        restart_button = Button(text="Перезапустить", font_size= 60, on_press=self.restart_game)
        self.layout.add_widget(restart_button)

    def restart_game(self, *_):
        self.layout.clear_widgets()
        self.__init__()
        self.layout.add_widget(self.build())

    def ranmise(self, player):
        rztmp = copy.deepcopy(self.razresh)
        for i in range(5):
            if rztmp[i]:
                player[i] = random.choice(rztmp[i])
                for el in rztmp:
                    if player[i] in el:
                        el.remove(player[i])
            else:
                return False
        return True

    def update(self, player):
        for i in range(5):
            del self.razresh[i][self.razresh[i].index(player[i])]

    def generate(self):
        self.players[0] = random.sample(self.seq, 5)
        for i in range(5):
            for img in self.seq:
                if img != self.players[0][i]:
                    self.razresh[i].append(img)

        for i in range(1, self.pl_count):
            flag2 = self.ranmise(self.players[i])
            while not flag2:
                flag2 = self.ranmise(self.players[i])
            self.update(self.players[i])


if __name__ == "__main__":
    MyApp().run()
