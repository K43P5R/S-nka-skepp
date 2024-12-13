"""
Program som simulerar spelet Sänka Skepp. Programmet har två klasser, en för skepp och en för spelplanen

skapad av Kasper Gundewall
"""
import random  # importera random för att slumpa kordinater
import os  # importera os för att kolla vilket operativsystem som används
from tkinter import Tk, Radiobutton, BooleanVar, StringVar, Label, Toplevel, Frame, Entry, LEFT # importera tkinter för att skapa grafiskt gränssnitt

if os.name == "posix":
    from tkmacosx import Button # importera tkmacosx för att lösa en bugg med tkinter på macos
                                    #Måste köra: pip install tkmacosx för att det ska fungera
                                    #Fick ideén från: https://www.reddit.com/r/learnpython/comments/13vkwh0/is_tkinter_too_broken_on_mac_to_be_usable/
else:  # om inte macos används
    from tkinter import Button

class Skepp:
    """Klass som representar varje skepp med attributen koord som är 
        skeppets kordinater och träffar som är de koordinater som är träffade
        Båda attrubuten är matrislistor som är 2 * skeppets längd"""

    def __init__(self, koord):
        self.koord = koord
        self.träffar = []  # tom lista där träffar kan läggas till
        self.territorium = []  # tom lista där skeppets territorium kan läggas till
        
class Spelplan(Tk):
    """Klass som representerar spelplanen med attributet skepp_på_plan
         som är en lista som innehåller objekt från klassen skepp"""
    
    def __init__(self):
        """Konstruktor som skapar en spelplan med skepp och knappar för att skjuta på skeppen"""
        super().__init__()
        self.topplista = []  # tomt lista där spelare och score kan läggas till
        with open("topplista.txt", "r", encoding = "utf-8") as fil:  # läser in topplistan från filen topplista.txt
            räkna = 1
            for rad in fil:
                rad = rad.strip()
                spelare, score = rad.split(":")  # spelare och score separeras från varandra då de är lagrade med ett ":" mellan dom
                self.topplista.append(f"{räkna}. {spelare}: {score}%\n")  
                räkna += 1
        
        self.title("Sänka Skepp")
        self.geometry("800x800")
        self.configure(background = "light blue")
        self.skepp_på_plan = []  # tom lista där skepp kan läggas till
        self.missar = []  # tom lista där missar kan läggas till
        self.generera_spelplan()  
        self.skapa_spelplan()
        self.fusk = BooleanVar()  # skapar en boolean variabel för att hålla koll på om fusk är på eller av
        self.fusk.set(False) 
        self.fusk_av_knapp = Radiobutton(self, text = "Fusk av", variable = self.fusk, value = False, 
        font = ("Helvetica", 20), bg = "light blue", fg = "black", command = self.fuska)  # Radioknappar som sätter av fusk och kallar på metoden fuska
        self.fusk_av_knapp.grid(column = 0, row = 0)
        self.fusk_på_knapp = Radiobutton(self, text = "Fusk på", variable = self.fusk, value = True, 
        font = ("Helvetica", 20), bg = "light blue", fg = "black", command = self.fuska)  #  Radioknappar som sätter på fusk och kallar på metoden fuska
        self.fusk_på_knapp.grid(column = 0, row = 1)
        self.räknare = 0  # variabel som räknar antalet skjutningar
        self.text_räknare = StringVar()  # för att visa antalet skjutningar på en label
        self.text_räknare_träffar = StringVar() # för att visa träffprocenten på en label
        self.text_räknare.set("Antal skjutningar: 0")
        self.text_räknare_träffar.set("Träffprocent: 0%")
        self.räkna_skjutningar = Label(self, textvariable = self.text_räknare, font = ("Helvetica", 20), bg = "light blue", fg = "black")
        self.räkna_skjutningar.grid(column = 0, row = 2)
        self.räkna_träffar = Label(self, textvariable = self.text_räknare_träffar, font = ("Helvetica", 20), bg = "light blue", fg = "black")
        self.räkna_träffar.grid(column = 0, row = 3)
        self.infomatation = Label(self, text = "Det finns 5 skepp med längderna 1 till 5 rutor", font = ("Helvetica", 20), bg = "light blue", fg = "black")
        self.infomatation.grid(column = 0, row = 4)
        self.avsluta = Button(self, text = "Avsluta utan att spara", font = ("Helvetica", 20), bg = "red", fg = "black",
        width = 200, height = 50, command = quit)
        if os.name == "nt":  # om inte macos används
            self.avsluta.config(width = 5, height = 1)
        self.avsluta.grid(column = 0, row = 5)

    def generera_spelplan(self):
        """Generar alla skepp på spelplanen med längder 2 - 6 och slumpmässiga kordinater"""
        for i in range(1, 6):  # loopar igenom skeppens längder
            while True:
                koord = []
                if i == 1:  # första skeppet behöver inte kolla intersektion
                    intersektion = False
                else:
                    intersektion = True
                x = random.randint(1, 10)  # slumpar x kordinaten
                y = random.randint(1, 10)  # slumpar y kordinaten
                riktning = random.choice(["x-led", "y-led"])  # slumpar riktning som skeppet ska byggas

                if riktning == "x-led":  # om skeppets koordnater byggs från vänster till höger
                    if x + i < 11:  # kollar så att skeppet inte hamnar utanför spelplanen
                        for j in range(i):
                            koord.append([x+j, y])
                        for skepp in self.skepp_på_plan:
                            for ruta in skepp.territorium:  # kollar om skeppet intersekterar med något annat skepp
                                if ruta in koord:
                                    intersektion = True
                                    break
                                intersektion = False
                            if intersektion is True:
                                break
                        if intersektion is False:
                            break

                elif riktning == "y-led":  # om skeppets koordnater byggs nedifrån och upp
                    if y + i < 11:  # kollar så att skeppet inte hamnar utanför spelplanen
                        for j in range(i):
                            koord.append([x, y+j])
                        for skepp in self.skepp_på_plan:
                            for ruta in skepp.territorium:
                                if ruta in koord:
                                    intersektion = True
                                    break
                                intersektion = False
                            if intersektion is True:
                                break  # hoppar ut ur while loopen om skeppet intersekterar med något annat skepp och börjar om i while loopen
                        if intersektion is False:
                            break  # hoppar ut ur while loopen om skeppet inte intersekterar med något annat skepp
            self.lägg_till_skepp(koord) # lägger till skepp på spelplanen

    def bygg_territorium(self, skepp):
        """Bygger skeppets territorium och kollar om skeppen intersekerar med varandra samt en parameter för att spara territoriumet
            om skeppet ska läggas till på spelplanen, 
            Returnerar True om skeppen intersekterar och False om skeppen inte intersekterar"""
        
        for ruta in skepp.koord:
            skepp.territorium.append(ruta)

            ruta_höger = [(ruta[0]+1), ruta[1]]
            skepp.territorium.append(ruta_höger)

            ruta_vänster = [(ruta[0]-1), ruta[1]]
            skepp.territorium.append(ruta_vänster)

            ruta_ovan = [ruta[0], (ruta[1]+1)]
            skepp.territorium.append(ruta_ovan)

            ruta_nedan = [ruta[0], (ruta[1]-1)]
            skepp.territorium.append(ruta_nedan)
        return skepp



    def lägg_till_skepp(self, koord):
        """Lägger till skepp på spelplanen"""
        koord.sort()
        nytt_skepp = Skepp(koord)
        nytt_skepp = self.bygg_territorium(nytt_skepp)
        self.skepp_på_plan.append(nytt_skepp)



    def skapa_spelplan(self):
        """Skapar spelplanen med knappar som representerar varje ruta/koordinat på spelplanen"""
        self.knappar = {}  # skapar ett tomt uppslagsverkör där kordinaterna är nyckelar till knapparna
        for x in range(1, 11):
            for y in range(1, 11):
                knapp = Button(self, text = "", font = ("Helvetica", 30), bg = "white", activebackground = "gray", 
                width = 50, height = 50, padx = 10, pady = 10, 
                command = lambda x = x, y = y: self.skjutning([x, y]))
                if os.name == "nt":
                    knapp.config(width = 3, height = 1, padx = 0, pady = 0)  # om windows används fungerar width och height annurlunda och andra värden används
                
                self.knappar[(x, y)] = knapp
                self.knappar[(x, y)].grid(column = x, row = (y + 30))

    def fuska(self):
        """Visar skeppens kordinater om fusk är på och tar bort skeppens obeskjutna kordinater om fusk är av"""
        for skepp in self.skepp_på_plan:
            for koord in skepp.koord:
                if koord not in skepp.träffar:  # för att inte änndra färgen på träffade skepp
                    x = koord[0]
                    y = koord[1]
                    if self.fusk.get() is True:
                        self.knappar[(x, y)].config(bg = "light green", text = "#")
                    else:
                        self.knappar[(x, y)].config(bg = "white", text = "")

    def skjutning(self, skjut_koord):
        """Kollar om skjutningen träffade något skepp samt om hela skeppet är träffat
            Felhantering för att inte skjuta på samma koordinat flera gånger"""
        if skjut_koord in self.missar:  # kollar om koordinaten redan är skuten på och missad
            return
        else:
            for skepp in self.skepp_på_plan:  # kollar om koordinaten redan är skuten på och träffad
                if skjut_koord in skepp.träffar:
                    return
        self.räknare += 1
        self.text_räknare.set(f"Antal skjutningar: {self.räknare}")  # uppdaterar antalet skjutningar

        x = skjut_koord[0]
        y = skjut_koord[1]
        for skepp in self.skepp_på_plan:  # loopar igenom alla skepp och kollar om skjutningen träffade något skepp
            if skjut_koord in skepp.koord:
                skepp.träffar.append(skjut_koord)  # lägger till träffen i skeppets träffar lista
                self.knappar[(x, y)].config(text = "X", bg = "red")  # ändrar färgen på knappen till röd
                self.text_räknare_träffar.set(f"Träffprocent: {round(((self.räknare - len(self.missar))/self.räknare)*100)}%")  # Variabeln som räknar träffar är i klassen skepp så det är effektivare subtracta antalet missar från antalet skjutningar
                self.kolla_hela_skepp_träffat(skepp)  # kollar om hela skeppet är träffat så att territorium kan visas
      
                return
        self.missar.append(skjut_koord)  # lägger till missen i missar listan om skjutningen inte träffade något skepp
        self.text_räknare_träffar.set(f"Träffprocent: {round(((self.räknare - len(self.missar))/self.räknare)*100)}%")  # Måste uppdateras efter missen blivit tillagd
        self.knappar[(x, y)].config(bg = "cyan")  # ändrar färgen på knappen till cyan
        return

    def kolla_hela_skepp_träffat(self, skepp):
        """Kollar om hela skeppet är träffat och visar skeppets territorium om det är träffat"""
        skepp.träffar.sort() # sorterar träffarna för att kunna jämföra med skeppets koordinater 
        if skepp.träffar == skepp.koord:  # om träffarna är lika med skeppets koordinater så är hela skeppet träffat
            for koord in skepp.territorium:
                if koord not in skepp.koord: # kollar så att koordinaten inte är en del av skeppet för att inte göra skeppet till cyan
                    x = koord[0]
                    y = koord[1]
                    if x > 0 and x < 11 and y > 0 and y < 11:  # kollar så att koordinaten i territoriumet inte är utanför spelplanen
                        self.knappar[(x, y)].config(bg = "cyan")  # ändrar färgen på knapparna i terri. till cyan
            self.framgång()
                
    def framgång(self):
        """Kollar om alla skepp är träffade och skapar en ny top level widget om alla skepp är träffade"""
        skjutna_skepp = 0  # variabel som räknar antalet träffade skepp
        for skepp in self.skepp_på_plan:  # kollar om alla skepp är träffade
            skepp.träffar.sort()
            if skepp.träffar == skepp.koord:
                skjutna_skepp += 1
        if skjutna_skepp == len(self.skepp_på_plan):  # om alla skepp är träffade
            self.score = round(((self.räknare - len(self.missar))/self.räknare)*100)  # räknar ut score
            self.notis = Toplevel(self)  # skapar en ny top level widget, fick ideén från: https://www.geeksforgeeks.org/python-tkinter-toplevel-widget/
            self.notis.geometry("400x150")
            self.notis.medelande = Label(self.notis, text = "Grattis! Du har sänkt alla skepp", font = ("Helvetica", 20))
            self.notis.medelande.pack()
            self.notis.gåvidare = Button(self.notis, text = "Gå vidare", font = ("Helvetica", 20), command = self.gör_topplista)
            self.notis.gåvidare.pack()
            for x in range(1, 11):
                for y in range(1, 11):
                    self.knappar[(x, y)].config(state = "disabled")  # gör alla knappar otryckbara när alla skepp är träffade så att räknaren inte ökar

    def gör_topplista(self, uppdatera = False):
        """Skapar en topplista med de 10 bästa spelarna och frågar om spelarens namn om spelaren är i top 10
            samt skickar med en parameter för att uppdatera topplistan till efter att spelaren skrivit in sitt namn"""
        for modul in self.winfo_children():  #  förstör alla widgets, fick ideén från:https://www.geeksforgeeks.org/how-to-clear-out-a-frame-in-the-tkinter/
            modul.destroy()
        self.avsluta2 = Button(self, text = "Avsluta", font = ("Helvetica", 20), bg = "red", fg = "black",
        width = 200, height = 50, command = quit)
        self.avsluta2.pack(side = LEFT)
        self.visa_topplista = Frame(self, width = 400, height = 800)
        self.visa_topplista.pack()  # anväder pack även fast jag använt grid tidigare men eftersom alla widgets är bortagna så borde inte grid och pack krocka
        self.visa_topplista.pack_propagate(False)
        self.visa_topplista.titel = Label(self.visa_topplista, text = "Topplista\n", font = ("Helvetica", 20))
        self.visa_topplista.titel.pack()
        for rad in self.topplista:
            self.visa_topplista.rad = Label(self.visa_topplista, text = rad, font = ("Helvetica", 18))
            self.visa_topplista.rad.pack()
        #Kollar om spelaren är i top 10 och frågar om spelarens namn om spelaren är i top 10, ska endast köras en gång
        if uppdatera is False:
            if len(self.topplista) < 10:  # om topplistan inte är fylld
                self.fråga_om_namn()
                return
            for rad in self.topplista:
                score = rad.split(":")[1]
                score = score.strip("%\n")
                if self.score > int(score):
                    self.fråga_om_namn()
                    return
        else:
            return
    
    def fråga_om_namn(self):
        """Skapar en ny top level widget där spelaren kan skriva in sitt namn"""
        self.skriv_in_namn = Toplevel(self)  # skapar en TopLevel widget för att skriva in namn
        self.skriv_in_namn.geometry("600x150")
        self.skriv_in_namn.gratulerar = Label(self.skriv_in_namn, text = f"Grattis! Du har sänkt alla skepp och fick en score på {self.score}% som är i top 10 bästa", font = ("Helvetica", 17))
        self.skriv_in_namn.gratulerar.pack()
        self.skriv_in_namn.namn_titel = Label(self.skriv_in_namn, text = "Skriv in ditt namn för att spara ditt namn i topplistan:", font = ("Helvetica", 17))
        self.skriv_in_namn.namn_titel.pack()
        self.namn = StringVar()
        self.skriv_in_namn.namn_entry = Entry(self.skriv_in_namn, textvariable = self.namn, font = ("Helvetica", 20))
        self.skriv_in_namn.namn_entry.pack()
        self.skriv_in_namn.skicka_ok = Button(self.skriv_in_namn, text = "OK", font = ("Helvetica", 20), command = self.spara)
        self.skriv_in_namn.skicka_ok.pack()

    def spara(self):
        """Sparar spelarens namn och poäng i topplistan och uppdaterar topplistan"""
        self.skriv_in_namn.destroy()
        lista_för_sortering = []  # tom lista som används för att sortera topplistan
        for rad in self.topplista:
            spelare, score = rad.split(":")
            spelare = spelare.split(".")[1]
            spelare = spelare.strip()
            score = score.strip("%\n")
            lista_för_sortering.append([int(score), spelare])
        lista_för_sortering.append([self.score, self.namn.get()])  # lägger till spelarens score och namn i listan
        lista_för_sortering = sorted(lista_för_sortering, key=lambda x: x[0], reverse = True)  # sorterar topplistan efter värdet i varje sublista, fick ideén från: https://www.geeksforgeeks.org/sorting-list-of-lists-with-first-element-of-each-sub-list-in-python/
        self.topplista = []  # tömmer topplistan för att sedan fylla på den med de sorterade värdena
        räkna = 1
        with open("topplista.txt", "w", encoding = "utf-8") as fil:  # skriver in topplistan i filen topplista.txt
            for rad in lista_för_sortering:
                score = rad[0]
                spelare = rad[1]
                fil.write(f"{spelare}:{score}\n")  # skriver in spelare och score i filen
                self.topplista.append(f"{räkna}. {spelare}: {score}%\n")  # för att kunna uppdatra topplistan i programmet
                räkna += 1
                if räkna == 11:  # bryter loopen när topp 10 spelare är sparade och sparar inte den sista spelaren
                    break
        self.gör_topplista(uppdatera = True)

def main():
    """Huvudfunktionen"""
    havsplan = Spelplan()
    havsplan.mainloop()

if __name__ == "__main__":
    main()
