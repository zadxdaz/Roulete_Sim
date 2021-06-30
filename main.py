import PySimpleGUI as sg
import random


class ruleta:
    def __init__(self,gui):
        self.colores = ["negro", "rojo", "celeste", "dorado"]
        self.chances = [25, 42, 52, 53]
        self.multipliers = [2, 3, 5, 50]
        self.max = 53
        self.bet = [0, 0, 0, 0]
        self.historial=[0,0,0,0]
        self.rondas=1
        self.balance=1000
        self.gui=gui
        self.image_color_link = [r"blacksquare.png", r"redsquare.png", r"lightbluesquare.png", r"goldsquare.png"]
        self.num=0
        self.wager=0

    def girar(self):
        self.num = random.randint(0, self.max)
    def guardar_color(self):
        self.historial[self.color()]+=1
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
    def run_sim(self,values):
        self.rondas += 1
        # tomar apuestas
        self.bet[0] = int(values.get("bet_negro"))
        self.bet[1] = int(values.get("bet_rojo"))
        self.bet[2] = int(values.get("bet_celeste"))
        self.bet[3] = int(values.get("bet_dorado"))
        self.wager_counter()
        for x in self.bet:
            self.balance -= x
        # girar ruleta
        self.girar()
        # guardar resultado
        self.guardar_color()
        self.balance += int(self.winnings())
    def update_gui(self):
        self.gui["imagen"].update(self.image_color_link[int(self.color())])
        self.gui["rondas"].update("Rondas:" + str(self.rondas))
        self.gui["balance"].update("Balance:\n" + str(self.balance))
        # actualizar el historial
        self.gui["historial negros"].update("Negros: " + str(self.historial[0])
                                       + " " + str(round(self.historial[0] * 100 / self.rondas, 2)))
        self.gui["historial rojos"].update("Rojos: " + str(self.historial[1])
                                      + " " + str(round(self.historial[1] * 100 / self.rondas, 2)))
        self.gui["historial celestes"].update("Celestes: " + str(self.historial[2])
                                         + " " + str(round(self.historial[2] * 100 / self.rondas, 2)))
        self.gui["historial dorados"].update("Dorados: " + str(self.historial[3])
                                        + " " + str(round(self.historial[3] * 100 / self.rondas, 2)))
        self.gui["wager_counter"].update("Wager: "+str(self.wager))
    def wager_counter(self):
        for x in self.bet:
            self.wager += x


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
    info_frame=[[sg.Text("Rondas:", key="rondas",size=(10,1))],
                [sg.Text("Wager: ",key="wager_counter",size=(10,1))]]
    balance_frame=[[sg.Text("Balance:", key="balance", size=(10, 5))],
                   [sg.Button("Add Balance")],
                   [sg.Input("0",key="add_balance_input")]]
    history_frame=[[sg.Text("Historial:")],
                   [sg.Text("Negros:",key="historial negros",size=(20,1))],
                   [sg.Text("Rojos:", key="historial rojos",size=(20,1))],
                   [sg.Text("Celestes:", key="historial celestes",size=(20,1))],
                   [sg.Text("Dorados:", key="historial dorados",size=(20,1))]]
    ultimo_color_frame = [[sg.Text("Color")],
                          [sg.Image(r"blacksquare.png", key="imagen", size=(100, 100))],
                          [sg.Button("Simular", target="imagen"),
                           sg.Button("Simulacion\nMasiva",key="massive_sim",size=(10,2))]]
    layout = [[sg.Frame("",balance_frame), sg.Frame("", ultimo_color_frame),
               sg.Frame("",info_frame),sg.Frame("",history_frame)],
              [sg.Frame("", negro_frame), sg.Frame("", rojo_frame), sg.Frame("", celeste_frame),
               sg.Frame("", dorado_frame)]]
    window = sg.Window("Menu", layout,finalize=True)
    return window

def main():
    menu = crear_menu()
    rulet = ruleta(menu)
    rulet.girar()
    rulet.guardar_color()
    rulet.update_gui()
    while True:
        event, values = menu.read()
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        if event == "Simular":
            rulet.run_sim(values)
            rulet.update_gui()
        if event == "massive_sim":
            for x in range(10000):
                rulet.run_sim(values)
            rulet.update_gui()
        if event == "Add Balance":
            rulet.balance += int(values.get("add_balance_input"))
            rulet.update_gui()



if __name__ == '__main__':
    main()
