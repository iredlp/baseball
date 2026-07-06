from database.DB_connect import DBConnect
from model.team import Team


class DAO():

        @staticmethod
        def getAllYears():
            conn = DBConnect.get_connection()

            result = []

            cursor = conn.cursor(dictionary=True)
            query = """select distinct(t.year )
                        from teams t 
                        where t.year>= 1980""" #query  NON parametrica perchè so già da prima che

            cursor.execute(query)

            for row in cursor:
                result.append(row["year"]) #lo leggo direttamente, non mi serve un oggetto per salvarli li

            cursor.close()
            conn.close()
            return result

        @staticmethod
        def getTeamsOfYear(year):
            conn = DBConnect.get_connection()

            result = []

            cursor = conn.cursor(dictionary=True)
            query = """ SELECT * 
                        FROM teams t
                        WHERE  t.YEAR=%s"""   #query parametrica

            cursor.execute(query, (year,))

            for row in cursor:
                result.append(Team(**row)) #CREO OGGETTO TEAM USANDO LE STESSE TABELLE DEL DB

            cursor.close()
            conn.close()
            return result

        @staticmethod
        def getSalariesTeam(year, idMapTeams):
            conn = DBConnect.get_connection()

            result = []

            cursor = conn.cursor(dictionary=True)
            query = """ select t.ID, t.teamCode, s.salary , sum(s.salary) as totSalary
                        from salaries s, teams t, appearances  a
                        where s.`year` = t.`year`  and t.`year` =a.`year`  and a.`year` =%s
                        and t.ID=a.teamID and a.playerID=s.playerID
                        group by t.ID, t.teamCode """  # query parametrica

            cursor.execute(query, (year,))

           # for row in cursor:
               # result.append((idMapTeams(row["ID"], row["totSalary"]))) #lista di tuple il cui primo elemento è un team e il secondo è un salario
            mapSalary={}
            #OPPURE POSSIAMO USARE UN DIZIONARIO PER NON DOVER CICLARE OGNI VOLTA
            for row in cursor:
                mapSalary[idMapTeams[row["ID"]]]=row["totSalary"] #chiave- team e valore- salari

            cursor.close()
            conn.close()
            return mapSalary





