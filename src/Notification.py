from mysql import get_db


class Notification():
    def __init__(self, user_id, message, link, is_read, notif_id=-1):
        self.notif_id = notif_id
        self.user_id = user_id
        self.message = message
        self.link = link
        self.is_read = is_read

    @staticmethod
    def add_new(user_id, message, link):
        notif = Notification(user_id, message, link, False)
        notif.insert()

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
    def get_unread_by_user_id(user_id):
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
            FROM Notifications WHERE user_id=%s AND is_read=FALSE
            """,
            [user_id]
        )
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
        return {
            "user_id": s[0],
            "message": s[1],
            "link": s[2],
            "is_read": s[3],
            "id": s[4]
        }

    def insert(self):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO Notifications (
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
            UPDATE Notifications
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
