from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import random
import copy
##

class MyApp(App):
    layout = BoxLayout(orientation="vertical")
    buttons = [
        Button(text="2 Игрока"),
        Button(text="3 Игрока"),
        Button(text="4 Игрока"),
        Button(text="Передай Игроку"),
    ]
    flag = False
    cnt = 0
    seq = ["A", "B", "C", "D", "E"]
    players = [
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""]
    ]
    razresh = [[], [], [], [], []]

    def build(self):
        self.flag = False
        self.cnt = 0
        self.layout.clear_widgets()
        self.buttons[3].text = "Передай Игроку"

        self.label = Label(text="Выберите кол-во игроков")
        self.layout.add_widget(self.label)

        self.create_button(self.buttons[0])
        self.create_button(self.buttons[1])
        self.create_button(self.buttons[2])
        return self.layout

    def create_button(self, button: Button):
        button.bind(on_press=self.button_press)
        self.layout.add_widget(button)

    def remove_button(self, button: Button):
        self.layout.remove_widget(button)

    def update_ui(self):
        self.buttons[3].bind(on_press=self.button_press_next)
        self.layout.add_widget(self.buttons[3])
        self.flag = True
        for i in range(3):
            self.remove_button(self.buttons[i])

    def button_press(self, instance):
        self.generate()
        self.cnt = int(instance.text[0]) + 100
        self.pl_count = int(instance.text[0])
        if not self.flag:
            self.update_ui()
        self.button_press_next(1)

    def button_press_next(self, instance):
        self.cnt -= 1   
        if self.cnt > 50:
            self.label.text = "Передай следующему!!!"
            self.cnt -= 99
        elif 0 <= self.cnt < 50:
            self.label.text = f"{self.pl_count - self.cnt} Игрок: {self.players[self.cnt]}"
            self.cnt += 100
        if self.cnt == 0:
            self.buttons[3].text = "Перезапустить"
            self.label.text = "Удачной игры!!!"         
        elif self.cnt == -1:
            self.players = [[""] * 5 for _ in range(4)]
            self.razresh = [[] for _ in range(5)]
            self.build()

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
            for alp in self.seq:
                if alp != self.players[0][i]:
                    self.razresh[i].append(alp)
        flag = self.ranmise(self.players[1])
        while not flag:
            flag = self.ranmise(self.players[1])
        self.update(self.players[1])
        flag = self.ranmise(self.players[2])
        while not flag:
            flag = self.ranmise(self.players[2])
        self.update(self.players[2])
        flag = self.ranmise(self.players[3])
        while not flag:
            flag = self.ranmise(self.players[3])
        print(*self.players, sep='\n')

if __name__ == "__main__":
    MyApp().run()
