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
        trenutni_predmet = moj_model.trenutno_potovanje.trenutni_predmet,
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
    return bottle.template("dodaj_potovanje.html", napake={}, polja={})


@bottle.post("/dodaj-novo-potovanje/")
def dodaj_potovanje_post():
    ime = bottle.request.forms.getunicode("ime")
    napake = {}
    polja = {"ime": ime}
    if not ime:
        napake['ime'] = 'Ime potovanja ne more biti prazno.'
    for potovanje in moj_model.potovanja:
        if potovanje.ime == ime:
            napake['ime'] = 'Izbrano ime je že zasedeno.'
    if napake:
        return bottle.template("dodaj_spisek.html", napake=napake, polja=polja)
    else:
        potovanje = Potovanje(ime)
        moj_model.dodaj_potovanje(potovanje)
        moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
        bottle.redirect("/")



@bottle.post("/zamenjaj-spakirano-predmeta/")
def spakiraj_predmet():
    indeks = bottle.request.forms.getunicode("indeks")
    predmet = moj_model.trenutno_potovanje.seznam_predmetov[int(indeks)]
    predmet.spakiraj_predmet()
    moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/")

@bottle.post("/zamenjaj-spakirano-predmeta/")
def spakiraj_predmet():
    indeks = bottle.request.forms.getunicode("indeks")
    podpredmet = moj_model.trenutno_potovanje.trenutni_predmet.seznam_podpredmetov[int(indeks)]
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



