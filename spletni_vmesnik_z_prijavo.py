import bottle
import os
from osnovne_funkcije_razredov import Popotnik, Potovanje, Predmet, Podpredmet

def nalozi_uporabnikovo_stanje():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    if uporabnisko_ime:
        return Popotnik.preberi_podatke_iz_datoteke(uporabnisko_ime)
    else:
        bottle.redirect("/prijava/")

def shrani_uporabnikovo_stanje(popotnik):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    popotnik.shrani_podatke_v_datoteko(uporabnisko_ime)


@bottle.get("/")
def osnovna_stran():
    popotnik = nalozi_uporabnikovo_stanje()
    return bottle.template(
        "osnovna_stran2.html",
        predmeti = popotnik.trenutno_potovanje.seznam_predmetov if popotnik.trenutno_potovanje else [],
        potovanja = popotnik.potovanja,
        trenutno_potovanje = popotnik.trenutno_potovanje,
        trenutni_predmet = popotnik.trenutno_potovanje.trenutni_predmet if popotnik.trenutno_potovanje else None,
        uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    )


@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napake={}, uporabnisko_ime=None)

@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    if os.path.exists(uporabnisko_ime):
        napake = {"uporabnisko_ime": "Uporabniško ime že obstaja."}
        return bottle.template("registracija.html", napake=napake, uporabnisko_ime=None)
    else:
        bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/")
        Popotnik().shrani_podatke_v_datoteko(uporabnisko_ime)
        bottle.redirect("/")


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napake={}, uporabnisko_ime=None)


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    if not os.path.exists(uporabnisko_ime):
        napake = {"uporabnisko_ime": "Uporabniško ime ne obstaja. Bi se radi regestrirali?"}
        return bottle.template("prijava.html", napake=napake, uporabnisko_ime=None)
    else:
        bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/")
        bottle.redirect("/")


@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie("uporabnisko_ime", path="/")
    print("piškotek uspešno pobrisan")
    bottle.redirect("/")

@bottle.get("/dodaj-novo-potovanje/")
def dodaj_potovanje_get():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    return bottle.template("dodaj_potovanje.html", uporabnisko_ime = uporabnisko_ime)

@bottle.post("/dodaj-novo-potovanje/")
def dodaj_potovanje_post():
    ime = bottle.request.forms.getunicode("ime")
    potovanje = Potovanje(ime)
    popotnik = nalozi_uporabnikovo_stanje()
    popotnik.dodaj_potovanje(potovanje)
    shrani_uporabnikovo_stanje(popotnik)
    bottle.redirect("/")


@bottle.get("/preimenuj-trenutno-potovanje/")
def preimenuj_trenutno_potovanje_get():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    return bottle.template("preimenuj_trenutno_potovanje.html", uporabnisko_ime=uporabnisko_ime)

@bottle.post("/preimenuj-trenutno-potovanje/")
def preimenuj_trenutno_potovanje_post():
    novo_ime = bottle.request.forms.getunicode("ime")
    popotnik = nalozi_uporabnikovo_stanje()
    potovanje = popotnik.trenutno_potovanje
    potovanje.ime = novo_ime
    shrani_uporabnikovo_stanje(popotnik)
    bottle.redirect("/")


@bottle.post("/zamenjaj-trenutno-potovanje/")
def zamenjaj_trenutno_potovanje():
    print(dict(bottle.request.forms))
    popotnik = nalozi_uporabnikovo_stanje()
    indeks = bottle.request.forms.getunicode("indeks")
    potovanje = popotnik.potovanja[int(indeks)]
    popotnik.trenutno_potovanje = potovanje
    shrani_uporabnikovo_stanje(popotnik)
    bottle.redirect("/")




@bottle.post("/dodaj-predmet/")
def dodaj_predmet():
    ime = bottle.request.forms.getunicode("ime")
    predmet = Predmet(ime)
    popotnik = nalozi_uporabnikovo_stanje()
    popotnik.dodaj_predmet(predmet)
    shrani_uporabnikovo_stanje(popotnik)
    bottle.redirect("/")


@bottle.get("/zamenjaj-stanje-predmeta/")
def stanje_predmeta_get():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    return bottle.template("zamenjaj_stanje_predmeta.html", napake={}, uporabnisko_ime = uporabnisko_ime)

@bottle.post("/zamenjaj-stanje-predmeta/")
def stanje_predmeta_post():
    stevilo = bottle.request.forms.getunicode("stevilo")
    popotnik = nalozi_uporabnikovo_stanje()
    predmet = popotnik.trenutno_potovanje.trenutni_predmet
    napake = {}
    if stevilo == "" or int(stevilo) not in [1,2,3]:
        napake["stevilo"] = "Vpisati je potrebno število med 1 in 3."

    if "stevilo" in napake:
        return bottle.template("zamenjaj_stanje_predmeta.html", napake=napake)
    else:

        if int(stevilo) == 1 and predmet.spakirano == False:
            predmet.spakiraj_predmet()
           
        elif int(stevilo) == 2 and predmet.zadnjaminuta == False:
            predmet.spakiraj_predmet_zadnjo_minuto()
    
        elif int(stevilo) == 3:
            if predmet.spakirano:
                predmet.spakiraj_predmet()
            elif predmet.zadnjaminuta:
                predmet.spakiraj_predmet_zadnjo_minuto()
    
    shrani_uporabnikovo_stanje(popotnik)
    bottle.redirect("/")


@bottle.post("/zamenjaj-trenutni-predmet/")
def zamenjaj_trenutni_predmet():
    print(dict(bottle.request.forms))
    popotnik = nalozi_uporabnikovo_stanje()
    indeks = bottle.request.forms.getunicode("indeks")
    predmet = popotnik.trenutno_potovanje.seznam_predmetov[int(indeks)]
    popotnik.trenutno_potovanje.trenutni_predmet = predmet
    shrani_uporabnikovo_stanje(popotnik)
    bottle.redirect("/")



@bottle.get("/dodaj-podpredmet/")
def dodaj_podpredmet_get():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    return bottle.template("dodaj_podpredmet.html", napake={}, uporabnisko_ime=uporabnisko_ime)

@bottle.post("/dodaj-podpredmet/")
def dodaj_podpredmet():
    ime = bottle.request.forms.getunicode("ime")
    stevilo = bottle.request.forms.getunicode("stevilo")
    popotnik = nalozi_uporabnikovo_stanje()
    podpredmet = Podpredmet(ime)
    napake = {}
    if stevilo == "" or int(stevilo) not in [1,2,3]:
        napake["stevilo"] = "Vpisati je potrebno število med 1 in 3."

    if "stevilo" in napake:
        return bottle.template("dodaj_podpredmet.html", napake=napake)

    else:

        if int(stevilo) == 1 and podpredmet.spakirano == False:
            podpredmet.spakiraj_podpredmet()
           
        elif int(stevilo) == 2 and podpredmet.zadnjaminuta == False:
            podpredmet.spakiraj_podpredmet_zadnjo_minuto()
    
        elif int(stevilo) == 3:
            if podpredmet.spakirano:
                podpredmet.spakiraj_podpredmet()
            elif podpredmet.zadnjaminuta:
                podpredmet.spakiraj_podpredmet_zadnjo_minuto()

    popotnik.dodaj_podpredmet(podpredmet)
    shrani_uporabnikovo_stanje(popotnik)
    bottle.redirect("/")


@bottle.get("/izbrisi-podpredmet/")
def izbrisi_podpredmet_get():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    popotnik = nalozi_uporabnikovo_stanje()

    return bottle.template("izbrisi_podpredmet.html", predmeti = popotnik.trenutno_potovanje.seznam_predmetov if popotnik.trenutno_potovanje else [],
        potovanja = popotnik.potovanja,
        trenutno_potovanje = popotnik.trenutno_potovanje,
        trenutni_predmet = popotnik.trenutno_potovanje.trenutni_predmet if popotnik.trenutno_potovanje else None, napake={}, uporabnisko_ime=uporabnisko_ime)

@bottle.post("/izbrisi-podpredmet/")
def izbrisi_podpredmet_post():
    stevilo = bottle.request.forms.getunicode("stevilo")
    popotnik = nalozi_uporabnikovo_stanje()
    
    dolzina = len(popotnik.trenutno_potovanje.trenutni_predmet.seznam_podpredmetov)
    napake = {}
    if stevilo == "" or int(stevilo) > dolzina or int(stevilo) < 1:
        napake["stevilo"] = f"Vpisati je potrebno število med 1 in {dolzina}."

    if "stevilo" in napake:
        return bottle.template("izbrisi_podpredmet.html", predmeti = popotnik.trenutno_potovanje.seznam_predmetov if popotnik.trenutno_potovanje else [],
        potovanja = popotnik.potovanja,
        trenutno_potovanje = popotnik.trenutno_potovanje,
        trenutni_predmet = popotnik.trenutno_potovanje.trenutni_predmet if popotnik.trenutno_potovanje else None, napake=napake)

    else:
        podpredmet = popotnik.trenutno_potovanje.trenutni_predmet.seznam_podpredmetov[int(stevilo)-1]
        popotnik.izbrisi_podpredmet(podpredmet)
        shrani_uporabnikovo_stanje(popotnik)
        bottle.redirect("/")



@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"


bottle.run(reloader=True, debug=True)



