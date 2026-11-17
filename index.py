import sys # za unos iz terminala
import math # za beskonacnost
import time
tkoPrviIgra = 1
brojCvorova = 0

DOBITNE_LINIJE = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # retci
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # stupci
    (0, 4, 8), (2, 4, 6)              # dijagonale
]

def potezi(polje):
    noviNiz = []
    for x in polje:
        if x.isdigit(): # ako je vrijednost neki broj, posavlja ju u novi niz
            noviNiz.append(x)
    return noviNiz

def ispisiPlocu(polje):
    i = 0
    print("--+---+---")
    for x in polje:
        if i < 2:
            print(x, end=" | ")
            i += 1
        else:
            print(x)
            i = 0

        if i == 0: # znamo sigurno da ce se nakon sto i == 2 on vratiti na 0, a ako smo tek usli u for petlju on sigurno ulazi u prvi if uvijet te se povecava prije nego sto dode do ovog if uvijeta
            print("--+---+---")

def terminal(polje):
    for a,b,c in DOBITNE_LINIJE:
        if polje[a] == polje[b] == polje[c] == "x": # provjerava sve mogucnosti gdje se moze pobjediti
            return True
        elif polje[a] == polje[b] == polje[c] == "o":
            return True
        elif len(potezi(polje)) == 0:
            return True

    return False

def pobjednik(polje):
    for a,b,c in DOBITNE_LINIJE:
        if polje[a] == polje[b] == polje[c] == "x": # provjerava sve mogucnosti gdje se moze pobjediti
            return "x"
        elif polje[a] == polje[b] == polje[c] == "o":
            return "o"

    return None

def utility(polje):
    global tkoPrviIgra
    znak = pobjednik(polje)
    if znak == "x" and tkoPrviIgra == 1: # ako racunalo igra prvo i pobjedio je x
        return 1
    elif znak == "x" and tkoPrviIgra == 0: # ako racunalo igra drugo i probjedio je x
        return -1
    elif znak == "o" and tkoPrviIgra == 1: # ako racunalo igra drugo i pobjedio je o
        return -1
    elif znak == "o" and tkoPrviIgra == 0: # ako racunalo igra drugo i pobjedio je o
        return 1

    return 0

def maxValue(polje, alpha, beta):
    global tkoPrviIgra, brojCvorova
    brojCvorova += 1
    if terminal(polje):
        return utility(polje)

    m = (-math.inf) # u - beskonacost
    slobodnaPolja = potezi(polje) # ispisivamo polja
    if tkoPrviIgra == 1:
        for a in slobodnaPolja:
            kopija = polje.copy()
            kopija[int(a)] = "x" # zauzimamo jedno mjesto u kopiranom polju
            m = max(m, minValue(kopija, alpha, beta)) # izabiremo najvecu vrijednost izmedu trenutne vrijednosti i nove
            if beta <= m: # ako nam je vrijednost u m veca od bete koju cuvamo, ulazimo u uvijet te prekidamo for petlju
                break
    else:
        for a in slobodnaPolja:
            kopija = polje.copy()
            kopija[int(a)] = "o"
            m = max(m, minValue(kopija, alpha, beta))
            if beta <= m:
                break

    beta = min(m, beta)
    return m

def minValue(polje, alpha, beta):
    global tkoPrviIgra, brojCvorova
    brojCvorova += 1
    if terminal(polje):
        return utility(polje)
    m = (math.inf)
    if tkoPrviIgra == 1:
        for x in potezi(polje):
            kopija = polje.copy()
            kopija[int(x)] = "o"
            m = min(m, maxValue(kopija, alpha, beta)) 
            if alpha >= m: # ako je vrijednost koju smo dobili je manja od alphe, prekidamo petlju
                break
    else:
        for x in potezi(polje):
            kopija = polje.copy()
            kopija[int(x)] = "x"
            m = min(m, maxValue(kopija, alpha, beta))
            if alpha >= m:
                break

    alpha = max(m, alpha)
    return m

def igraRacunalo(polje):
    global tkoPrviIgra, brojCvorova
    brojCvorova = 0
    najboljiBrojIndexa = None
    if tkoPrviIgra == 1:
        znak = "x"
    else:
        znak = "o"
    m = (-math.inf)
    beta = (math.inf)
    alpha = (-math.inf)
    pocetak = time.perf_counter() # timer pocetak
    # pravimo kopiju za svaki novi potez, svaki potez nam vraca najbolju vrijednost, vrijednost koja bude najbolja pamtimo njen index
    for a in potezi(polje):
        kopija = polje.copy()
        kopija[int(a)] = znak
        v = minValue(kopija, alpha, beta)
        if v > m:
            m = v
            najboljiBrojIndexa = a
    kraj = time.perf_counter() # timer kraj
    polje[int(najboljiBrojIndexa)] = znak
    trajanje = kraj - pocetak
    ispisiPlocu(polje)
    print("Računalo igra potez ",najboljiBrojIndexa," (vrijednost:",m,", čvorova: ",brojCvorova,", vrijeme: ",trajanje," s")
    return polje

if __name__ == "__main__":
    polje= ["0","1","2",
            "3","4","5",
            "6","7","8"] # matrica za pozicije

    nastavi = True # zastavica za provjeru unosa iz terminala
    if "--racunalo" in sys.argv:
        print("Prvo racunalo igra")
        tkoPrviIgra = 1
    elif "--covjek" in sys.argv:
        print("Prvo covjek igra")
        tkoPrviIgra = 0
    else:
        print("Molimo ispravan unos")
        nastavi = False

    if nastavi:
        ispisiPlocu(polje)
        print("----------------------")
        if tkoPrviIgra == 1:
            while terminal(polje) == False:
                polje = igraRacunalo(polje)

                # ako igra završi s zadnjim potezom od covjeka vise nece biti mjesta na ploci, onda racunalo ulazi da postavi znak i izbaciva error
                if terminal(polje) == True:
                    if utility(polje) == 1:
                        print("Pobjeda računala")
                    elif utility(polje) == 0:
                        print("Nerješeno")
                    else:
                        print("Pobjeda čovjeka")
                    break

                potez = input("Izaberite na kojem indexu želite postaviti o: ")
                while not potez in potezi(polje):
                    potez = input("Molimo vas unesite slobodni index")
                polje[int(potez)] = "o"
                ispisiPlocu(polje)
                print("------------------")

                if terminal(polje) == True:
                    if utility(polje) == 1:
                        print("Pobjeda računala")
                    elif utility(polje) == 0:
                        print("Nerješeno")
                    else:
                        print("Pobjeda čovjeka")
                    break

        elif tkoPrviIgra == 0:
            while terminal(polje) == False:
                potez = input("Izaberite na kojem indexu želite postaviti x: ")
                while not potez in potezi(polje):
                    potez = input("Molimo vas unesite slobodni index")
                polje[int(potez)] = "x"
                ispisiPlocu(polje)
                print("-----------------")

                # ako igra završi s zadnjim potezom od covjeka vise nece biti mjesta na ploci, onda racunalo ulazi da postavi znak i izbaciva error
                if terminal(polje) == True:
                    if utility(polje) == 1:
                        print("Pobjeda računala")
                    elif utility(polje) == 0:
                        print("Nerješeno")
                    else:
                        print("Pobjeda čovjeka")
                    break

                polje = igraRacunalo(polje)

                if terminal(polje) == True:
                    if utility(polje) == 1:
                        print("Pobjeda računala")
                    elif utility(polje) == 0:
                        print("Nerješeno")
                    else:
                        print("Pobjeda čovjeka")
                    break