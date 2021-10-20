from osnovne_funkcije_razredov import Popotnik, Potovanje, Predmet, Podpredmet


DATOTEKA_ZA_SHRANJEVANJE = 'popotnik.json'
try:
    moj_model = Popotnik.preberi_podatke_iz_datoteke(DATOTEKA_ZA_SHRANJEVANJE)
except FileNotFoundError:
    moj_model = Popotnik()

DODAJ_POTOVANJE = 1
IZBRISI_POTOVANJE = 2
ZAMENJAJ_POTOVANJE = 3
PREIMENUJ_POTOVANJE = 4
DODAJ_PREDMET = 5
IZBRISI_PREDMET = 6
SPAKIRAJ_PREDMET = 7
SPAKIRAJ_PREDMET_ZADNJO_MINUTO = 8
ZAMENJAJ_TRENUTNI_PREDMET =  9
DODAJ_PODPREDMET = 10
SPAKIRAJ_PODPREDMET = 11
SPAKIRAJ_PODPREDMET_ZADNJO_MINUTO = 12
IZBRISI_PODPREDMET = 13
IZHOD = 14

def preberi_izbrano_stevilo():
    while True:
        uporabnikov_vnos = input('> ')
        try:
            return int(uporabnikov_vnos)
        except ValueError:
            print ('Prosim vnesite število.')


def izberi_ukaz(ukazi):
    for stevilo, (ukaz, opis) in enumerate(ukazi, 1):
        print (f'{stevilo} -> {opis}')
    while True:
        stevilo = preberi_izbrano_stevilo()
        if 1 <= stevilo <= len(ukazi):
            (ukaz, opis) = ukazi[stevilo - 1]
            return ukaz
        else:
            print (f'Prosim, da izberete število med 1 in {len(ukazi)}!')


def prikaz_potovanja(potovanje):
        odstotek_potovanja = potovanje.odstotek_spakiranja()
        return f'>{potovanje.ime.upper()}<  {odstotek_potovanja} %'

def prikaz_predmeta(predmet):
    if predmet.seznam_podpredmetov == []:
        if predmet.zadnjaminuta:
            return f'{predmet.ime.upper()}!!'
        else:
            return f'{predmet.ime}'
    else:
        odstotek = predmet.odstotek_spakiranja_podpredmetov()
        return f'{predmet.ime}  {odstotek} %'

def prikaz_podpredmeta(podpredmet):
    if podpredmet.zadnjaminuta:
        return f'{podpredmet.ime.upper()}!!'
    else:
        return f'{podpredmet.ime}'


def izberi_predmet(popotnik):
    vse_izbire_predmetov = []
    for predmet in popotnik.trenutno_potovanje.seznam_predmetov:
        par = (predmet, prikaz_predmeta(predmet))
        vse_izbire_predmetov.append(par)
    return izberi_ukaz(vse_izbire_predmetov)

def izberi_potovanje(popotnik):
    vse_izbire_potovanj = []
    for potovanje in popotnik.potovanja:
        par = (potovanje, prikaz_potovanja(potovanje))
        vse_izbire_potovanj.append(par)
    return izberi_ukaz(vse_izbire_potovanj)

#        if isinstance(podkategorija, Podkategorija):

def izberi_podpredmet(popotnik):
    vse_izbire_podpredmetov = []
    for podpredmet in popotnik.trenutno_potovanje.trenutni_predmet.seznam_podpredmetov:
        par = (podpredmet, prikaz_podpredmeta(podpredmet))
        vse_izbire_podpredmetov.append(par)
    return izberi_ukaz(vse_izbire_podpredmetov)


def pozdrav():
    print('Pozdravljen popotnik!')


def tekstovni_vmesnik():
    pozdrav()
    while True:
        prikazi_trenutni_seznam_predmetov()
        izbira = izberi_ukaz(
            [
                (DODAJ_POTOVANJE, 'dodaj novo potovanje'),
                (IZBRISI_POTOVANJE, 'izbriši potovanje'),
                (ZAMENJAJ_POTOVANJE, 'izberi drugo potovanje'),
                (PREIMENUJ_POTOVANJE, 'preimenuj potovanje'),
                (DODAJ_PREDMET, 'dodaj nov predmet'),
                (IZBRISI_PREDMET, 'izbriši predmet'),
                (SPAKIRAJ_PREDMET, 'spakiraj predmet'),
                (SPAKIRAJ_PREDMET_ZADNJO_MINUTO, 'predmet spakiraj zadnjo minuto'),
                (ZAMENJAJ_TRENUTNI_PREDMET, 'zamenjaj predmet'),
                (DODAJ_PODPREDMET, 'dodaj nov predmet v skupino predmetov'),
                (SPAKIRAJ_PODPREDMET, 'spakiraj predmet v skupini predmetov'),
                (SPAKIRAJ_PODPREDMET_ZADNJO_MINUTO, 'predmet v skupini predmetov spakiraj zadnjo minuto'),
                (IZBRISI_PODPREDMET, 'izbriši predmet v skupini predmetov'),
                (IZHOD, 'zaključi pakiranje')
            ]
        )
        if izbira == DODAJ_POTOVANJE:
            dodaj_potovanje()

        if izbira == IZBRISI_POTOVANJE:
            izbrisi_potovanje()

        if izbira == ZAMENJAJ_POTOVANJE:
            zamenjaj_potovanje()

        if izbira == PREIMENUJ_POTOVANJE:
            preimenuj_potovanje()

        if izbira == DODAJ_PREDMET:
            dodaj_predmet()

        if izbira == IZBRISI_PREDMET:
            izbrisi_predmet()

        if izbira == SPAKIRAJ_PREDMET:
            spakiraj_predmet()

        if izbira == SPAKIRAJ_PREDMET_ZADNJO_MINUTO:
            spakiraj_predmet_zadnjo_minuto()

        if izbira == ZAMENJAJ_TRENUTNI_PREDMET:
            zamenjaj_trenutni_predmet()

        if izbira == DODAJ_PODPREDMET:
            dodaj_podpredmet()

        if izbira == SPAKIRAJ_PODPREDMET:
            spakiraj_podpredmet()

        if izbira == SPAKIRAJ_PODPREDMET_ZADNJO_MINUTO:
            spakiraj_podpredmet_zadnjo_minuto()

        if izbira == IZBRISI_PODPREDMET:
            izbrisi_podpredmet()

        if izbira == IZHOD:
            moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
            print('Bon Voyage!')
            break



def prikazi_trenutni_seznam_predmetov():
    if moj_model.trenutno_potovanje:
        print (f'{prikaz_potovanja(moj_model.trenutno_potovanje)}')
        for predmet in moj_model.trenutno_potovanje.seznam_predmetov:
            if predmet.seznam_podpredmetov == []:
                if not predmet.spakirano:
                    print (f'- {prikaz_predmeta(predmet)}')
                else:
                    print (f'> {prikaz_predmeta(predmet)}')
            else:
                print (f'- {prikaz_predmeta(predmet)}')
                for podpredmet in predmet.seznam_podpredmetov:
                    if not podpredmet.spakirano:
                        print (f'    + {prikaz_podpredmeta(podpredmet)}')
                    else:
                        print (f'    > {prikaz_podpredmeta(podpredmet)}')

    else:
        print ('Trenutno nimate nobenega aktivngea potovanja, zato morate izbrati enega od obstoječih ali pa ustvariti novega.')
        moznosti = [('DODAJ', 'Dodaj novo potovanje.'), ('ZAMENJAJ', 'Izberi obstoječe potovanje.')]
        if izberi_ukaz(moznosti) == 'DODAJ':
            dodaj_potovanje()
        else:
            izberi_trenutno_potovanje()


def izberi_trenutno_potovanje():
    trenutno = izberi_potovanje(moj_model)
    moj_model.trenutno_potovanje = trenutno
    prikazi_trenutni_seznam_predmetov()


def dodaj_potovanje():
    print ('Vnesite ime novega potovanja.')
    ime = input('Ime> ')
    seznam = []
    novo_potovanje = Potovanje(ime, seznam)
    moj_model.dodaj_potovanje(novo_potovanje)

def izbrisi_potovanje():
    potovanje = izberi_potovanje(moj_model)
    moj_model.izbrisi_potovanje(potovanje)

def zamenjaj_potovanje():
    print ('Izberite enega izmed vaših potovanj.')
    potovanje = izberi_potovanje(moj_model)
    moj_model.zamenjaj_trenutno_potovanje(potovanje)

def preimenuj_potovanje():
    print ('Vnesite novo ime potovanja.')
    novo_ime = input('Novo ime> ')
    moj_model.preimenuj_potovanje(novo_ime)

def dodaj_predmet():
    print ('Vnesite ime novega predmeta.')
    ime = input('Ime> ')
    nov_predmet = Predmet(ime)
    moj_model.dodaj_predmet(nov_predmet)

def izbrisi_predmet():
    if moj_model.trenutno_potovanje.seznam_predmetov == []:
        print (f'Izbranega ukaza ni mogoče izvesti, saj nimate še nobenega dodanega predmeta!')
    else:
        predmet = izberi_predmet(moj_model)
        moj_model.izbrisi_predmet(predmet)

def spakiraj_predmet():
    if moj_model.trenutno_potovanje.seznam_predmetov == []:
        print (f'Izbranega ukaza ni mogoče izvesti, saj nimate še nobenega dodanega predmeta!')
    else:
        predmet = izberi_predmet(moj_model)
        if predmet.seznam_podpredmetov == []:
            predmet.spakiraj_predmet()
        else:
            print (f'Ukaza ni mogoče izvesti na predmetu, ki predstavlja skupino.')

def spakiraj_predmet_zadnjo_minuto():
    if moj_model.trenutno_potovanje.seznam_predmetov == []:
        print (f'Izbranega ukaza ni mogoče izvesti, saj nimate še nobenega dodanega predmeta!')
    else:
        predmet = izberi_predmet(moj_model)
        if predmet.seznam_podpredmetov == []:
            predmet.spakiraj_predmet_zadnjo_minuto()
        else:
            print (f'Ukaza ni mogoče izvesti na predmetu, ki predstavlja skupino.')

       

def zamenjaj_trenutni_predmet():
    if moj_model.trenutno_potovanje.seznam_predmetov == []:
        print (f'Izbranega ukaza ni mogoče izvesti, saj nimate še nobenega dodanega predmeta!')
    else:
        print ('Izberite enega izmed vaših obstoječih predmetov.')
        novi_trenutni = izberi_predmet(moj_model)
        moj_model.zamenjaj_trenutni_predmet(novi_trenutni)

def dodaj_podpredmet():
    print('Vnesite ime novega predmeta, ki ga želite dodati v skupino.')
    ime = input('Ime> ')
    nov_podpredmet = Podpredmet(ime)
    moj_model.dodaj_podpredmet(nov_podpredmet)

def izbrisi_podpredmet():
    if moj_model.trenutno_potovanje.trenutni_predmet.seznam_podpredmetov == []:
        print (f'Izbranega ukaza ni mogoče izvesti, saj v tej skupini nimate dodanega še nobenega predmeta.')
    else:
        podpredmet = izberi_podpredmet(moj_model)
        moj_model.izbrisi_podpredmet(podpredmet)

def spakiraj_podpredmet():
    if moj_model.trenutno_potovanje.trenutni_predmet.seznam_podpredmetov == []:
        print (f'Izbranega ukaza ni mogoče izvesti, saj v tej skupini nimate dodanega še nobenega predmeta.')
    else:    
        podpredmet = izberi_podpredmet(moj_model)
        podpredmet.spakiraj_podpredmet()

def spakiraj_podpredmet_zadnjo_minuto():
    if moj_model.trenutno_potovanje.trenutni_predmet.seznam_podpredmetov == []:
        print (f'Izbranega ukaza ni mogoče izvesti, saj v tej skupini nimate dodanega še nobenega predmeta.')
    else:
        podpredmet = izberi_podpredmet(moj_model)
        podpredmet.spakiraj_podpredmet_zadnjo_minuto()


tekstovni_vmesnik()