import json


class Popotnik:
    def __init__(self):
        self.potovanja = [Gore(), Morje(), Ogled_mesta(), Smucanje()]
        self.trenutno_potovanje = None

    def zamenjaj_trenutno_potovanje(self, potovanje):
        self.trenutno_potovanje = potovanje

    def dodaj_potovanje(self, potovanje):
        self.potovanja.append(potovanje)
        self.trenutno_potovanje = potovanje

    def izbrisi_potovanje(self, potovanje):
        self.potovanja.remove(potovanje)

    def preimenuj_potovanje(self, novo_ime):
        self.trenutno_potovanje.preimenuj_potovanje(novo_ime)

    def dodaj_predmet(self, predmet):
        self.trenutno_potovanje.dodaj_predmet(predmet)

    def zamenjaj_trenutni_predmet(self, predmet):
        self.trenutno_potovanje.zamenjaj_trenutni_predmet(predmet)

    def izbrisi_predmet(self, predmet):
        self.trenutno_potovanje.izbrisi_predmet(predmet)

    def dodaj_podpredmet(self, podpredmet):
        self.trenutno_potovanje.trenutni_predmet.dodaj_podpredmet(podpredmet)

    def izbrisi_podpredmet(self, podpredmet):
        self.trenutno_potovanje.trenutni_predmet.izbrisi_podpredmet(podpredmet)

    def odstotek_spakiranja(self, potovanje):
        self.odstotek_spakiranja(potovanje)
    
    def v_slovar(self):
        vsa_potovanja = []
        for potovanje in self.potovanja:
            vsa_potovanja.append(potovanje.v_slovar())
        if self.trenutno_potovanje:
            trenutno = self.potovanja.index(self.trenutno_potovanje)
        else:
            trenutno = None
        return {
            'potovanja': vsa_potovanja,
            'trenutno_potovanje': trenutno
        }

    @staticmethod
    def iz_slovarja(slovar):
        popotnik = Popotnik()
        popotnikova_potovanja = []
        for potovanje_v_slovarju in slovar['potovanja']:
            popotnikova_potovanja.append(Potovanje.iz_slovarja(potovanje_v_slovarju))
        
        popotnik.potovanja = popotnikova_potovanja
        if slovar['trenutno_potovanje'] != None:
            popotnik.trenutno_potovanje = popotnik.potovanja[slovar['trenutno_potovanje']]
        return popotnik

    def shrani_podatke_v_datoteko(self, datoteka):
        with open(datoteka, 'w', encoding='utf-8') as file:
            slovar = self.v_slovar()
            json.dump(slovar, file)
    
    @staticmethod
    def preberi_podatke_iz_datoteke(datoteka):
        with open(datoteka, encoding='utf-8') as file:
            slovar = json.load(file)
            return Popotnik.iz_slovarja(slovar)



class Potovanje:
    def __init__(self, ime, seznam = []):
        self.ime = ime
        self.seznam_predmetov = seznam
        self.trenutni_predmet = None

    def __repr__(self):
        return f'{self.ime}'
    
    def dodaj_predmet(self, predmet):
        self.seznam_predmetov.append(predmet)
        self.trenutni_predmet = predmet

    def izbrisi_predmet(self, predmet):
        self.seznam_predmetov.remove(predmet)
        
    def zamenjaj_trenutni_predmet(self, predmet):
        self.trenutni_predmet = predmet

    def preimenuj_potovanje(self, novo_ime):
        self.ime = novo_ime

    def odstotek_spakiranja(self):
        stevilo_vseh_predmetov = 0
        stevilo_spakiranih_predmetov = 0
        for predmet in self.seznam_predmetov:
            if predmet.seznam_podpredmetov == []:
                stevilo_vseh_predmetov += 1
                if predmet.spakirano == True:
                    stevilo_spakiranih_predmetov += 1
            else:
                for podpredmet in predmet.seznam_podpredmetov:
                    stevilo_vseh_predmetov += 1
                    if podpredmet.spakirano == True:
                        stevilo_spakiranih_predmetov += 1
        
        if stevilo_vseh_predmetov == 0:
            odstotek = 0
        else:
            nezaokrozen = (stevilo_spakiranih_predmetov / stevilo_vseh_predmetov) * 100
            odstotek = round(nezaokrozen, 1)
        return odstotek

    #def odstotek_spakiranja_podpredmetov(self):
    #    stevilo_vseh_podpredmetov = len(self.seznam_podpredmetov)
    #    stevilo_spakiranih_podpredmetov = 0
    #    for podpredmet in self.seznam_podpredmetov:
    #        if podpredmet.spakirano == True:
    #            stevilo_spakiranih_podpredmetov += 1
    #    odstotek = (stevilo_spakiranih_podpredmetov / stevilo_vseh_podpredmetov) * 100
    #    return round(odstotek, 1)

    def v_slovar(self):
        ime = self.ime
        seznam_predmetov = []
        for predmet in self.seznam_predmetov:
            seznam_predmetov.append(predmet.v_slovar())
        if self.trenutni_predmet:
            trenutni_predmet = self.seznam_predmetov.index(self.trenutni_predmet)
        else:
            trenutni_predmet = None

        return {
            'ime': ime,
            'seznam_predmetov': seznam_predmetov,
            'trenutni_predmet': trenutni_predmet
        }

    @staticmethod
    def iz_slovarja(slovar):
        potovanje = Potovanje(slovar['ime'])

        seznam = []
        for predmet_v_slovarju in slovar['seznam_predmetov']:
            seznam.append(Predmet.iz_slovarja(predmet_v_slovarju))

        potovanje.seznam_predmetov = seznam
        return potovanje


class Gore(Potovanje):
    def __init__(self):
        super().__init__('Gore', preberi_datoteko('gore.txt')) 

class Morje(Potovanje):
    def __init__(self):
        super().__init__('Morje', preberi_datoteko('morje.txt'))

class Ogled_mesta(Potovanje):
    def __init__(self):
        super().__init__('Ogled mesta', preberi_datoteko('ogled_mesta.txt'))

class Smucanje(Potovanje):
    def __init__(self):
        super().__init__('Smučanje', preberi_datoteko('smucanje.txt'))



class Predmet:
    def __init__(self, ime):
        self.ime = ime
        self.spakirano = False
        self.zadnjaminuta = False
        self.seznam_podpredmetov = []
        
    def __repr__(self):
        return self.ime

    def spakiraj_predmet(self):
        self.spakirano = True

    def spakiraj_predmet_zadnjo_minuto(self):
        self.zadnjaminuta = True

    def dodaj_podpredmet(self, podpredmet):
        self.seznam_podpredmetov.append(podpredmet)

    def izbrisi_podpredmet(self, podpredmet):
        self.seznam_podpredmetov.remove(podpredmet)

    def odstotek_spakiranja_podpredmetov(self):
        stevilo_vseh_podpredmetov = len(self.seznam_podpredmetov)
        stevilo_spakiranih_podpredmetov = 0
        for podpredmet in self.seznam_podpredmetov:
            if podpredmet.spakirano == True:
                stevilo_spakiranih_podpredmetov += 1
        odstotek = (stevilo_spakiranih_podpredmetov / stevilo_vseh_podpredmetov) * 100
        return round(odstotek, 1)
    

    def v_slovar(self):
        ime = self.ime
        spakirano = self.spakirano
        spakirano_zadnjo_minuto = self.zadnjaminuta

        seznam = []
        for podpredmet in self.seznam_podpredmetov:
            seznam.append(podpredmet)

        return {
            'ime': ime,
            'spakirano': spakirano,
            'spakirano_zadnjo_minuto': spakirano_zadnjo_minuto,
            'seznam_podpredmetov': seznam
        }

    @staticmethod
    def iz_slovarja(slovar):
        predmet = Predmet(slovar['ime'])

        seznam = []
        for podpredmet_v_slovarju in slovar['seznam_podpredmetov']:
            seznam.append(Podpredmet.iz_slovarja(podpredmet_v_slovarju))
        predmet.seznam_podpredmetov = seznam

        predmet.spakirano = slovar['spakirano']
        predmet.zadnjaminuta = slovar['spakirano_zadnjo_minuto']

        return predmet



class Podpredmet:
    def __init__(self, ime):
        self.ime = ime
        self.spakirano = False
        self.zadnjaminuta = False

    def spakiraj_podpredmet(self):
        self.spakirano = True

    def spakiraj_podpredmet_zadnjo_minuto(self):
        self.zadnjaminuta = True

    
    def v_slovar(self):
        ime = self.ime
        spakirano = self.spakirano
        spakirano_zadnjo_minuto = self.zadnjaminuta
        return {
            'ime': ime,
            'spakirano': spakirano,
            'spakirano_zadnjo_minuto' : spakirano_zadnjo_minuto
        }

    @staticmethod
    def iz_slovarja(slovar):
        podpredmet = Podpredmet(slovar['ime'])
        podpredmet.spakirano = slovar['spakirano']
        podpredmet.zadnjaminuta = slovar['spakirano_zadnjo_minuto']
        return podpredmet


def preberi_datoteko(ime):
    with open(ime, encoding='utf8') as datoteka:
        seznam_predmetov = []
        for i in datoteka.readline().split(','):
            seznam_predmetov.append(Predmet(i))
        return seznam_predmetov    