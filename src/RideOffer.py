from mysql import get_db, format_date


class RideOffer():
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": ["string", "null"]},
            "max_seats": {"type": "number"},
            "open_seats": {"type": "number"},
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
        self.max_seats = j["max_seats"]
        self.open_seats = j["open_seats"]
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
            "max_seats": self.max_seats,
            "open_seats": self.open_seats,
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
                MaxSeats,
                OpenSeats,
                StartDateTime,
                EndDateTime,
                OriginName,
                OriginLat,
                OriginLng,
                DestinationName,
                DestinationLat,
                DestinationLng
            FROM Offers
            """)
        response_list = map(RideOffer.sql_response_to_json, cur.fetchall())
        return response_list

    @staticmethod
    def get_with_id(offer_id):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            SELECT
                Id,
                Title,
                MaxSeats,
                OpenSeats,
                StartDateTime,
                EndDateTime,
                OriginName,
                OriginLat,
                OriginLng,
                DestinationName,
                DestinationLat,
                DestinationLng
            FROM Offers WHERE Id=%s
            """, [offer_id])
        return RideOffer.sql_response_to_json(cur.fetchall()[0])

    @staticmethod
    def sql_response_to_json(s):
        return {
            "id": s[0],
            "title": s[1],
            "max_seats": s[2],
            "open_seats": s[3],
            "start_time": str(s[4].time()),
            "start_date": str(s[4].date()),
            "end_time": str(s[5].time()),
            "end_date": str(s[5].date()),
            "origin": {
                "name": s[6],
                "lat": s[7],
                "lng": s[8]
            },
            "destination": {
                "name": s[9],
                "lat": s[10],
                "lng": s[11]
            }
        }

    @staticmethod
    def from_sql_response(s):
        return RideOffer(RideOffer.sql_response_to_json(s))

    def insert(self):
        db = get_db()
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO Offers (
              Title,
              MaxSeats,
              OpenSeats,
              StartDateTime,
              EndDateTime,
              OriginName,
              OriginLat,
              OriginLng,
              DestinationName,
              DestinationLat,
              DestinationLng
            ) VALUES (%s, %s, %s, $s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                self.title,
                self.max_seats,
                self.open_seats,
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
            UPDATE Offers
            SET
              Title=%s,
              MaxSeats=%s,
              OpenSeats=%s,
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
                self.max_seats,
                self.open_seats,
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
    def delete_with_id(offer_id):
        db = get_db()
        cur = db.cursor()
        cur.execute("DELETE FROM Offers WHERE Id=%s", [offer_id])
        db.commit()
