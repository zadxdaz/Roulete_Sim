import PySimpleGUI as sg
import random


class ruleta:
    def __init__(self):
        self.colores = ["negro", "rojo", "celeste", "dorado"]
        self.chances = [25, 42, 52, 53]
        self.multipliers = [2, 3, 5, 50]
        self.max = 53
        self.bet = [0, 0, 0, 0]

    def girar(self):
        self.num = random.randint(0, self.max)
        print(self.num)
    def color(self):
        for x in range(len(self.chances)):
            if self.num <= self.chances[x]:
                return x
    def winnings(self):
        self.profit = int(self.multipliers[int(self.color())]) * int(self.bet[int(self.color())])
        return self.profit
    def losses(self):
        self.lose=0
        for x in range(len(self.colores)):
            if x == self.color():
                continue
            else :
                self.lose += int(self.bet[x])
        print(self.lose)
        return self.lose

def bet_frame(color):
    key = "bet_" + color
    frame = [[sg.Text(color)],
             [sg.Input("0", key=key, size=(10, 100))]]
    return frame

def crear_menu():
    negro_frame = bet_frame("negro")
    rojo_frame = bet_frame("rojo")
    celeste_frame = bet_frame("celeste")
    dorado_frame = bet_frame("dorado")

    ultimo_color_frame = [[sg.Text("Color")],
                          [sg.Image(r"blacksquare.png", key="imagen", size=(100, 100))],
                          [sg.Button("Simular", target="imagen")]]

    layout = [[sg.Text("Balance:", key="balance", size=(10, 5)), sg.Frame("", ultimo_color_frame),
               sg.Text("Rondas:", key="rondas",size=(10,5))],
              [sg.Frame("", negro_frame), sg.Frame("", rojo_frame), sg.Frame("", celeste_frame),
               sg.Frame("", dorado_frame)]]
    window = sg.Window("Menu", layout,finalize=True)
    return window


def main():
    rulet = ruleta()
    rondas = 0
    menu = crear_menu()
    balance = 1000
    image_color_link = [r"blacksquare.png", r"redsquare.png", r"lightbluesquare.png", r"goldsquare.png"]
    menu["balance"].update("Balance:\n"+str(balance))
    menu["rondas"].update("Rondas:" + str(rondas))
    while True:
        event, values = menu.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        rondas += 1
        # tomar apuestas
        rulet.bet[0] = int(values.get("bet_negro"))
        rulet.bet[1] = int(values.get("bet_rojo"))
        rulet.bet[2] = int(values.get("bet_celeste"))
        rulet.bet[3] = int(values.get("bet_dorado"))
        for x in rulet.bet:
            balance -= x
        # girar ruleta
        rulet.girar()
        balance += int(rulet.winnings())
        menu["imagen"].update(image_color_link[int(rulet.color())])
        menu["rondas"].update("Rondas:"+str(rondas))
        menu["balance"].update("Balance:\n" + str(balance))




if __name__ == '__main__':
    main()
