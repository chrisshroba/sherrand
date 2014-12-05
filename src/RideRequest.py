from mysql import get_db, format_date


class RideRequest():
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": ["string", "null"]},
            "user_id": {"type": "number"},
            "start_time": {"type": "string"},
            "start_date": {"type": "string"},
            "end_time": {"type": "string"},
            "end_date": {"type": "string"},
            "origin": {
                "type": "object",
                "properties": {
                    "name": {"type": ["string", "null"]},
                    "lat": {"type": "number"},
                    "lng": {"type": "number"}
                },
                "required": ["lat", "lng"]
            },
            "destination": {
                "type": "object",
                "properties": {
                    "name": {"type": ["string", "null"]},
                    "lat": {"type": "number"},
                    "lng": {"type": "number"}
                },
                "required": ["lat", "lng"]
            }
        },
        "required": ["user_id", "start_time", "start_date", "end_time", "end_date", "origin", "destination"]
    }

    def __init__(self, j):
        self.id = j["id"] if "id" in j else None
        self.title = j["title"] if "title" in j else None
        self.user_id = j["user_id"]
        self.start_time = j["start_time"]
        self.start_date = j["start_date"]
        self.end_time = j["end_time"]
        self.end_date = j["end_date"]
        self.origin = {
            "name": j["origin"]["name"] if "name" in j["origin"] else None,
            "lat": j["origin"]["lat"],
            "lng": j["origin"]["lng"]
        }
        self.destination = {
            "name": j["destination"]["name"] if "name" in j["destination"] else None,
            "lat": j["destination"]["lat"],
            "lng": j["destination"]["lng"]
        }

    def to_json_object(self):
        return {
            "title": self.title,
            "user_id": self.user_id,
            "start_time": self.start_time,
            "start_date": self.start_date,
            "end_time": self.end_time,
            "end_date": self.end_date,
            "origin": self.origin,
            "destination": self.destination
        }

    @staticmethod
    def get_all():
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            SELECT
                Id,
                Title,
                User,
                StartDateTime,
                EndDateTime,
                OriginName,
                OriginLat,
                OriginLng,
                DestinationName,
                DestinationLat,
                DestinationLng
            FROM Requests
            """)
        response_list = map(RideRequest.sql_response_to_json, cur.fetchall())
        return response_list

    @staticmethod
    def get_with_id(request_id):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            SELECT
                Id,
                User,
                Title,
                StartDateTime,
                EndDateTime,
                OriginName,
                OriginLat,
                OriginLng,
                DestinationName,
                DestinationLat,
                DestinationLng
            FROM Requests WHERE Id=%s
            """, [request_id])
        return RideRequest.sql_response_to_json(cur.fetchall()[0])


    @staticmethod
    def sql_response_to_json(s):
        return {
            "id": s[0],
            "title": s[1],
            "user_id": s[2],
            "start_time": str(s[3].time()),
            "start_date": str(s[3].date()),
            "end_time": str(s[4].time()),
            "end_date": str(s[4].date()),
            "origin": {
                "name": s[5],
                "lat": s[6],
                "lng": s[7]
            },
            "destination": {
                "name": s[8],
                "lat": s[9],
                "lng": s[10]
            }
        }
    @staticmethod
    def from_sql_response(s):
        return RideRequest(RideRequest.sql_response_to_json(s))

    def insert(self):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO Requests (
              Title,
              User,
              StartDateTime,
              EndDateTime,
              OriginName,
              OriginLat,
              OriginLng,
              DestinationName,
              DestinationLat,
              DestinationLng
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                self.title,
                self.user_id,
                format_date(self.start_date, self.start_time),
                format_date(self.end_date, self.end_time),
                self.origin["name"],
                self.origin["lat"],
                self.origin["lng"],
                self.destination["name"],
                self.destination["lat"],
                self.destination["lng"]
            )
        )
        db.commit()
        cur = db.cursor()
        cur.execute("SELECT MAX(Id) FROM Requests")
        res = cur.fetchall()[0][0]
        return res

    def update(self):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            UPDATE Requests
            SET
              Title=%s,
              User=%s,
              StartDateTime=%s,
              EndDateTime=%s,
              OriginName=%s,
              OriginLat=%s,
              OriginLng=%s,
              DestinationName=%s,
              DestinationLat=%s,
              DestinationLng=%s
            WHERE Id=%s
            """,
            (
                self.title,
                self.user_id,
                format_date(self.start_date, self.start_time),
                format_date(self.end_date, self.end_time),
                self.origin["name"],
                self.origin["lat"],
                self.origin["lng"],
                self.destination["name"],
                self.destination["lat"],
                self.destination["lng"],
                self.id
            )
        )
        db.commit()

    @staticmethod
    def delete_with_id(request_id):
        db = get_db()
        cur = db.cursor()
        cur.execute("DELETE FROM Requests WHERE Id=%s", [request_id])
        db.commit()
