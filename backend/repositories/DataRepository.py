from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_status_lampen():
        sql = "SELECT * from lampen"
        return Database.get_rows(sql)

    @staticmethod
    def read_status_lamp_by_id(id):
        sql = "SELECT * from lampen WHERE id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_status_lamp(id, status):
        sql = "UPDATE lampen SET status = %s WHERE id = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_status_alle_lampen(status):
        sql = "UPDATE lampen SET status = %s"
        params = [status]
        return Database.execute_sql(sql, params)

    @staticmethod
    def get_user(uid):
        sql = "SELECT UserID FROM tblusers WHERE RFIDKey = %s"
        params = [uid]
        return Database.get_one_row(sql, params)

    @staticmethod
    def insert_historiek_play(id, datum):
        sql = "INSERT tblhistoriek (Datum, User) VALUES (%s,%s)"
        params = [datum, id]
        return Database.execute_sql(sql, params)
    @staticmethod
    def update_historiek_play(playtime, datum):
        sql = "UPDATE tblhistoriek SET PlayTime = %s WHERE Datum = %s"
        params = [playtime, datum]
        return Database.execute_sql(sql, params)

    @staticmethod
    def get_historiek(id_user=1):
        sql = "SELECT Datum, PlayTime FROM tblhistoriek WHERE User = %s ORDER BY Datum DESC LIMIT 7"
        params = [id_user]
        return Database.get_rows(sql, params)

    @staticmethod
    def get_live_decibels():
        sql = "SELECT DecibelWaarde FROM tbldecibels  ORDER BY DecibelsID DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def insert_decibels(waarde):
        sql= "INSERT tbldecibels (DecibelWaarde, DateTime, tblHistoriek_HistoriekID) VALUES (%s, NOW(), (SELECT HistoriekID FROM tblhistoriek  ORDER BY HistoriekID DESC LIMIT 1) ) "
        params = [waarde]
        return Database.execute_sql(sql, params)