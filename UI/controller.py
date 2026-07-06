import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

       # self._fillDDYears() SE LO METTO QUI SBAGLIO!!!!

    def handleCreaGrafo(self, e):
        pass

    def handleDettagli(self, e):
        pass

    def handlePercorso(self, e):
        pass

    def _fillDDYears(self):
        years=self._model.getAllYears()
        #li metto nel dropdown

        #yearsDD=[]
        #for y in years:
          #  yearsDD.append(ft.dropdown.Option(y)) #li aggiungo uno alla volta

        #OPPURE USO IL METODO MAP
        yearsDD= list(map( lambda x: ft.dropdown.Option(str(x)), years)) #applico la lambda function agli elementi della lista
        #la lambda function sostituisce li elementi con ft.dropdown.Option

        #NB SE NON METTO MAP NELLA LISTA, RESTITUISCE un consumabile- nel momento in cui ci ciclo una  volta vengono svuotati
        self._view._ddAnno.options = yearsDD
        self._view.update_page()
       # self._view._page.update()

    def handleYearsSelecion(self, e):
        #questo metodo viene chiamato quando qualcuno ha selezionato un anno
        #deve recuperare tutti i team che hanno giocato quell'anno e stamparli nel tectfield
        # e riempire i dropdown sotto
        if self._view._ddAnno.value is None:
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSquadre.controls.append(ft.Text("Seleziona un anno dal menu"))

        teams=self._model.getTeamsOfYear(self._view._ddAnno.value)


        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Per il {self._view._ddAnno.value} sono"
                                                          f" iscritte al campionato {len(teams)} squadre "))

        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(t))

        self._view.update_page()






