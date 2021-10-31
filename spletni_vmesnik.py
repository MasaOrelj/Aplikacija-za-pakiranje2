import bottle

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
        trenutni_predmet = moj_model.trenutno_potovanje.trenutni_predmet if moj_model.trenutno_potovanje else None
    )



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


@bottle.get("/preimenuj-trenutno-potovanje/")
def preimenuj_trenutno_potovanje_get():
    return bottle.template("preimenuj_trenutno_potovanje.html")

@bottle.post("/preimenuj-trenutno-potovanje/")
def preimenuj_trenutno_potovanje_post():
    novo_ime = bottle.request.forms.getunicode("ime")
    potovanje = moj_model.trenutno_potovanje
    potovanje.ime = novo_ime
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




@bottle.post("/dodaj-predmet/")
def dodaj_predmet():
    ime = bottle.request.forms.getunicode("ime")
    predmet = Predmet(ime)
    moj_model.dodaj_predmet(predmet)
    moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/")


@bottle.get("/zamenjaj-stanje-predmeta/")
def stanje_predmeta_get():
    return bottle.template("zamenjaj_stanje_predmeta.html", napake={})

@bottle.post("/zamenjaj-stanje-predmeta/")
def stanje_predmeta_post():
    stevilo = bottle.request.forms.getunicode("stevilo")
    predmet = moj_model.trenutno_potovanje.trenutni_predmet
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



@bottle.get("/dodaj-podpredmet/")
def dodaj_podpredmet_get():
    return bottle.template("dodaj_podpredmet.html", napake={})

@bottle.post("/dodaj-podpredmet/")
def dodaj_podpredmet():
    ime = bottle.request.forms.getunicode("ime")
    stevilo = bottle.request.forms.getunicode("stevilo")
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

    moj_model.dodaj_podpredmet(podpredmet)
    moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
    bottle.redirect("/")


@bottle.get("/izbrisi-podpredmet/")
def izbrisi_podpredmet_get():
    return bottle.template("izbrisi_podpredmet.html", predmeti = moj_model.trenutno_potovanje.seznam_predmetov if moj_model.trenutno_potovanje else [],
        potovanja = moj_model.potovanja,
        trenutno_potovanje = moj_model.trenutno_potovanje,
        trenutni_predmet = moj_model.trenutno_potovanje.trenutni_predmet if moj_model.trenutno_potovanje else None, napake={})

@bottle.post("/izbrisi-podpredmet/")
def izbrisi_podpredmet_post():
    stevilo = bottle.request.forms.getunicode("stevilo")
    
    dolzina = len(moj_model.trenutno_potovanje.trenutni_predmet.seznam_podpredmetov)
    napake = {}
    if stevilo == "" or int(stevilo) > dolzina or int(stevilo) < 1:
        napake["stevilo"] = f"Vpisati je potrebno število med 1 in {dolzina}."

    if "stevilo" in napake:
        return bottle.template("izbrisi_podpredmet.html", predmeti = moj_model.trenutno_potovanje.seznam_predmetov if moj_model.trenutno_potovanje else [],
        potovanja = moj_model.potovanja,
        trenutno_potovanje = moj_model.trenutno_potovanje,
        trenutni_predmet = moj_model.trenutno_potovanje.trenutni_predmet if moj_model.trenutno_potovanje else None, napake=napake)

    else:
        podpredmet = moj_model.trenutno_potovanje.trenutni_predmet.seznam_podpredmetov[int(stevilo)-1]
        moj_model.izbrisi_podpredmet(podpredmet)
        moj_model.shrani_podatke_v_datoteko(DATOTEKA_ZA_SHRANJEVANJE)
        bottle.redirect("/")



@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"


bottle.run(reloader=True, debug=True)



