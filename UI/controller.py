import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceTeam=None

       # self._fillDDYears() SE LO METTO QUI SBAGLIO!!!!

    def handleCreaGrafo(self, e):
        self._model.creaGrafo(self._view._ddAnno.value)
        n,m=self._model.getGraphDetails()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato! "
                                                       f"Il grafo è costituito da {n} modi e {m} archi"))
        self._view.update_page()

    def handleDettagli(self, e):
        if self._choiceTeam is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Selezionare un team dal menu ", color="red"))
            self._view.update_page()
            return
        viciniTuple=self._model.getVicini(self._choiceTeam)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Il nodo{self._choiceTeam} ha {len(viciniTuple)} vicini", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Di seguito una lista ordinata di vicini", color="green"))
        for v in viciniTuple:
            self._view._txt_result.controls.append(ft.Text(f"{v[0]}- peso: {v[1]}", color="green"))
        self._view.update_page()



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
        #CHE SONO ANCHE I NODI DEL GRAFO

        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Per il {self._view._ddAnno.value} sono"
                                                          f" iscritte al campionato {len(teams)} squadre "))

        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(t))
            #ciclo anche nel dropdown per aggiornare
            self._view._ddSquadra.options.append(ft.dropdown.Option(data=t,
                                                                    text=t.name, on_click=self.readDDTeams))

        self._view.update_page()


    def readDDTeams(self, e):
        if e.control.data is None:
            self._choiceTeam=None
        else:
            self._choiceTeam=e.control.data
        print(f"Selezionato il team{self._choiceTeam}")


