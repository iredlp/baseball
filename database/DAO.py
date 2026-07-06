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




