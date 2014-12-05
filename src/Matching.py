from mysql import get_db
from Notification import Notification


def check_for_matches_request(new_request):
    origin_name = new_request["origin"]["name"]
    origin_lat = new_request["origin"]["lat"]
    origin_lng = new_request["origin"]["lng"]
    dest_name = new_request["destination"]["name"]
    dest_lat = new_request["destination"]["lat"]
    dest_lng = new_request["destination"]["lng"]
    start_date = new_request["start_date"]
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        SELECT
          Id, (
            3959 * acos (
              cos ( radians(%s) )
              * cos( radians( OriginLat ) )
              * cos( radians( OriginLng ) - radians(%s) )
              + sin ( radians(%s) )
              * sin( radians( OriginLat ) )
            )
          ) AS origin_distance,
          (
            3959 * acos (
              cos ( radians(%s) )
              * cos( radians( DestinationLat ) )
              * cos( radians( DestinationLng ) - radians(%s) )
              + sin ( radians(%s) )
              * sin( radians( DestinationLat ) )
            )
          ) AS dest_distance,
          OriginName, DestinationName, StartDateTime
        FROM Offers
        HAVING
            (origin_distance < 1 OR OriginName=%s)
            AND (dest_distance < 1 OR DestinationName=%s)
            AND DATE(StartDateTime)=%s
        """,
        (
            origin_lat, origin_lng, origin_lat,
            dest_lat, dest_lng, dest_lat,
            origin_name,
            dest_name,
            start_date
        )
    )
    results = cur.fetchall()
    for res in results:
        Notification.add_new(new_request["user_id"], "New ride offer available to " + dest_name + "!", "/offer/" + str(res[0]))


def check_for_matches_offer(new_offer):
    origin_name = new_offer["origin"]["name"]
    origin_lat = new_offer["origin"]["lat"]
    origin_lng = new_offer["origin"]["lng"]
    dest_name = new_offer["destination"]["name"]
    dest_lat = new_offer["destination"]["lat"]
    dest_lng = new_offer["destination"]["lng"]
    start_date = new_offer["start_date"]
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        SELECT
          User, (
            3959 * acos (
              cos ( radians(%s) )
              * cos( radians( OriginLat ) )
              * cos( radians( OriginLng ) - radians(%s) )
              + sin ( radians(%s) )
              * sin( radians( OriginLat ) )
            )
          ) AS origin_distance,
          (
            3959 * acos (
              cos ( radians(%s) )
              * cos( radians( DestinationLat ) )
              * cos( radians( DestinationLng ) - radians(%s) )
              + sin ( radians(%s) )
              * sin( radians( DestinationLat ) )
            )
          ) AS dest_distance,
          OriginName, DestinationName, StartDateTime
        FROM Requests
        HAVING
            (origin_distance < 1 OR OriginName=%s)
            AND (dest_distance < 1 OR DestinationName=%s)
            AND DATE(StartDateTime)=%s
        """,
        (
            origin_lat, origin_lng, origin_lat,
            dest_lat, dest_lng, dest_lat,
            origin_name,
            dest_name,
            start_date
        )
    )
    results = cur.fetchall()
    for res in results:
        Notification.add_new(res[0], "New ride offer available to " + dest_name + "!", "/offer/" + str(new_offer["id"]))
