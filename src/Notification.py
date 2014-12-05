from mysql import get_db, format_date


class Notification():
    def __init__(self, user_id, message, link, is_read, notif_id=-1):
        self.notif_id = notif_id
        self.user_id = user_id
        self.message = message
        self.link = link
        self.is_read = is_read

    @staticmethod
    def get_all():
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            SELECT
                user_id,
                message,
                link,
                is_read,
                id
            FROM Notifications
            """)
        response_list = map(Notification.from_sql_response, cur.fetchall())
        return response_list

    @staticmethod
    def get_with_id(notif_id):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            SELECT
                user_id,
                message,
                link,
                is_read,
                id
            FROM Notifications WHERE id=%s
            """, [notif_id])
        return Notification.from_sql_response(cur.fetchall()[0])

    @staticmethod
    def from_sql_response(s):
        return Notification(s[0], s[1], s[2], s[3], s[5])

    def insert(self):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO Offers (
                user_id,
                message,
                link,
                is_read
            ) VALUES (%s, %s, %s, %s)
            """,
            (
                self.user_id,
                self.message,
                self.link,
                self.is_read
            )
        )
        db.commit()

    def update(self):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            UPDATE Offers
            SET
              user_id=%s,
              message=%s,
              link=%s,
              is_read=%s
            WHERE id=%s
            """,
            (
                self.user_id,
                self.message,
                self.link,
                self.is_read
            )
        )
        db.commit()

    @staticmethod
    def delete_with_id(notif_id):
        db = get_db()
        cur = db.cursor()
        cur.execute("DELETE FROM Notifications WHERE id=%s", [notif_id])
        db.commit()
