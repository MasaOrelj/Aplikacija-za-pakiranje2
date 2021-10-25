import bottle
import os
from osnovne_funkcije_razredov import Popotnik, Potovanje, Predmet, Podpredmet

DATOTEKA_ZA_SHRANJEVANJE = 'popotnik.json'
try:
    moj_model = Popotnik.preberi_podatke_iz_datoteke(DATOTEKA_ZA_SHRANJEVANJE)
except FileNotFoundError:
    moj_model = Popotnik()


@bottle.get("/")
def osnovna_stran():
    return bottle.template(
        "osnovna_stran.html",
        predmeti = moj_model.trenutno_potovanje.seznam_predmetov if moj_model.trenutno_potovanje else [],
        potovanja = moj_model.potovanja,
        trenutno_potovanje = moj_model.trenutno_potovanje,
        trenutni_predmet = moj_model.trenutno_potovanje.trenutni_predmet
    )

@bottle.post("/dodaj-predmet/")
def dodaj_predmet():
    ime = bottle.request.forms.getunicode("ime")
    predmet = Predmet(ime)
    moj_model.dodaj_predmet(predmet)
    moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/")


@bottle.get("/dodaj-podpredmet/")
def dodaj_podpredmet_get():
    return bottle.template("dodaj_podpredmet.html")

@bottle.post("/dodaj-podpredmet/")
def dodaj_podpredmet():
    ime = bottle.request.forms.getunicode("ime")
    podpredmet = Podpredmet(ime)
    moj_model.dodaj_podpredmet(podpredmet)
    moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/")

@bottle.get("/dodaj-novo-potovanje/")
def dodaj_potovanje_get():
    return bottle.template("dodaj_potovanje.html")


@bottle.post("/dodaj-novo-potovanje/")
def dodaj_potovanje_post():
    ime = bottle.request.forms.getunicode("ime")
    potovanje = Potovanje(ime)
    moj_model.dodaj_potovanje(potovanje)
    moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/")



@bottle.post("/zamenjaj-stanje-predmeta/")
def stanje_predmeta():
    indeks = bottle.request.forms.getunicode("indeks")
    predmet = moj_model.trenutno_potovanje.seznam_predmetov[int(indeks)]
    if predmet.spakirano == False and predmet.zadnjaminuta == False:
        predmet.spakiraj_predmet()
    elif predmet.spakirano == True:
        predmet.spakiraj_predmet_zadnjo_minuto()
    elif predmet.zadnjaminuta == True:
        predmet.spakiraj_predmet_zadnjo_minuto()

    moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/")

@bottle.post("/zamenjaj-stanje-podpredmeta/")
def stanje_podpredmeta():
    indeks = bottle.request.forms.getunicode("indeks")
    podpredmet = moj_model.trenutno_potovanje.trenutni_predmet.seznam_podpredmetov[int(indeks)]
    if podpredmet.spakirano == False and podpredmet.zadnjaminuta == False:
        podpredmet.spakiraj_predmet()
    elif podpredmet.spakirano == True:
        podpredmet.spakiraj_predmet_zadnjo_minuto()
    elif podpredmet.zadnjaminuta == True:
        podpredmet.spakiraj_predmet_zadnjo_minuto()

    podpredmet.spakiraj_podpredmet()
    moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/")



@bottle.post("/zamenjaj-trenutno-potovanje/")
def zamenjaj_trenutno_potovanje():
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    potovanje = moj_model.potovanja[int(indeks)]
    moj_model.trenutno_potovanje = potovanje
    moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/")

@bottle.post("/zamenjaj-trenutni-predmet/")
def zamenjaj_trenutni_predmet():
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    predmet = moj_model.trenutno_potovanje.seznam_predmetov[int(indeks)]
    moj_model.trenutno_potovanje.trenutni_predmet = predmet
    moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/")



@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"


bottle.run(reloader=True, debug=True)



