import simplejson as json
from geopy.distance import vincenty

HOME = (47.810640, -122.245335)
WORK = (47.615879, -122.336312)
MAX_DISTANCE_METERS = 1000


def load_trips(filename):
    trips = json.load(open(filename))
    return trips


def trip_as_csv(trip, dir):
    return ",".join([
        trip['id'],
        str(trip['started_at']),
        str(trip['ended_at']),
        str(trip['duration_s']),
        dir
    ])


def run(trips_json):
    trips = load_trips(trips_json)

    for trip in trips:
        start = (trip['start_location']['lat'], trip['start_location']['lon'])
        end = (trip['end_location']['lat'], trip['end_location']['lon'])

        # from A to B or from B to A
        if vincenty(start, HOME).meters < MAX_DISTANCE_METERS and vincenty(end, WORK).meters < MAX_DISTANCE_METERS:
            print(trip_as_csv(trip, 'work'))
        elif vincenty(start, WORK).meters < MAX_DISTANCE_METERS and vincenty(end, HOME).meters < MAX_DISTANCE_METERS:
            print(trip_as_csv(trip, 'home'))


if __name__ == '__main__':
    run('trips.json')
