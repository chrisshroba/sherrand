from mysql import get_db, format_date


class RideRequest():
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": ["string", "null"]},
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
        "required": ["start_time", "start_date", "end_time", "end_date", "origin", "destination"]
    }

    def __init__(self, j):
        self.id = j["id"] if "id" in j else None
        self.title = j["title"] if "title" in j else None
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
            "start_time": str(s[2].time()),
            "start_date": str(s[2].date()),
            "end_time": str(s[3].time()),
            "end_date": str(s[3].date()),
            "origin": {
                "name": s[4],
                "lat": s[5],
                "lng": s[6]
            },
            "destination": {
                "name": s[7],
                "lat": s[8],
                "lng": s[9]
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
              StartDateTime,
              EndDateTime,
              OriginName,
              OriginLat,
              OriginLng,
              DestinationName,
              DestinationLat,
              DestinationLng
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                self.title,
                format_date(self.start_date, self.start_time),
                format_date(self.end_date, self.end_time),
                self.origin["name"],
                self.origin["lat"],
                self.origin["lng"],
                self.destination["name"],
                self.destination["lat"],
                self.destination["lng"],
            )
        )
        db.commit()

    def update(self):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            UPDATE Requests
            SET
              Title=%s,
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