# Križić-Kružić AI (Minimax + Alpha-Beta podrezivanje)

Konzolna implementacija igre Križić-kružić (Tic-Tac-Toe) u Pythonu protiv nepobjedive umjetne inteligencije. AI koristi **Minimax algoritam** optimiziran **Alpha-Beta podrezivanjem** kako bi u svakom trenutku odabrao matematički optimalan potez uz minimalan broj pretraženih stanja.

## Značajke

* **Optimalna igra:** Algoritam evaluira buduća stanja ploče (`+1` za pobjedu računala, `0` za remi, `-1` za pobjedu čovjeka) i nikada ne gubi partiju.
* **Fleksibilan početak partije:** Putem argumenata u terminalu bira se igra li prvo računalo ili čovjek.
* **Analiza performansi:** Nakon svakog poteza računala ispisuje se odabrani indeks, procijenjena vrijednost poteza, ukupan broj posjećenih čvorova u stablu te vrijeme izračuna u sekundama (`time.perf_counter`).

## Učinak Alpha-Beta podrezivanja

Dodavanjem `alpha` i `beta` granica algoritam rano odbacuje grane stabla koje ne mogu utjecati na konačnu odluku, čime se drastično smanjuje broj evaluiranih stanja na prvom potezu (kada je ploča potpuno prazna):

| Algoritam | Obiđeni čvorovi (1. potez) | Smanjenje pretrage |
| :--- | :---: | :---: |
| Čisti Minimax | ~549.946 | — |
| Minimax + Alpha-Beta | ~18.000 – 21.000 | ~96 % |

## Pokretanje programa

Projekt koristi isključivo ugrađene Python biblioteke (`sys`, `math`, `time`) i ne zahtijeva instalaciju dodatnih paketa.

**1. Računalo igra prvo (kao `x`):**
```bash
py index.py --racunalo
