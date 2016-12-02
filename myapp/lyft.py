# ---------------------------------------------------------------------------
import logging
import requests
from spyne.application import Application
from spyne.decorator import srpc
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
from spyne.service import ServiceBase


class Lyft(ServiceBase):

    # get total cost from string given as parameter
    # SAMPLE CALL : 127.0.0.1:5000/gettotalcost?strng=3,37.7772,-122.4233,37.7972,-122.4533,37.7772,-122.4233
    @srpc(str,str,_returns = unicode)
    def gettotalcost(self, strng):
        lat = []
        lng = []
        cords = strng.split(',')
        # fetching the no of locations to be covered
        no_of_cords = int(cords[0])
        count = 0
        # yield len(cords)
        # yield cords[0]

        #setting the lat and lng list from the string given as a parameter
        while count < no_of_cords:
            lat.append(cords[(2*count) + 1])
            lng.append(cords[(2*count) + 2])

            count += 1


        # dictionary for each type of ride
        lyft = {'min_cost': 0,
                'max_cost': 0,
                'time': 0,
                'distance': 0,
                'type':'lyft'
                }
        lyft_line = {'min_cost': 0,
                     'max_cost': 0,
                     'time': 0,
                     'distance': 0,
                     'type':'lyft_line'

                     }
        lyft_plus = {'min_cost': 0,
                     'max_cost': 0,
                     'time': 0,
                     'distance': 0,
                     'type': 'lyft_plus'
                     }
        lyft_premier = {'min_cost': 0,
                        'max_cost': 0,
                        'time': 0,
                        'distance': 0,
                        'type' : 'lyft_premier'
                        }
        cheapest = {
            'cost': 0,
            'distance': 0,
            'time' : 0,
            'type' :''
        }

        # making call for ride between each 2 sets of (lat,lng)
        count = 0
        while count != (no_of_cords -1):

            payload = {'start_lat': lat[count], 'start_lng': lng[count], 'end_lat': lat[count + 1], 'end_lng': lng[count + 1]}
            headers = {
                'Authorization': 'Bearer gAAAAABYOh2rXUfRCrbLM5kt_kICcQvAuyefz_9pJsgGhHQLhKnu3idO-pEgZN6xBWRqXyy0vaOFPse2Rk4i26RCUhKOBvYvnXAW17OwAGpmXdEzG_38O-sYbz9zd_OHdswBrRXFGKy9lBflP0eVWLP3rsCQJd1JuBFJdks2AfawYNAviW1wB2s=',
                'Accept-Language': 'en_US',
                'Content-Type': 'application/json',
            }

            stop = requests.get(
                'https://api.lyft.com/v1/cost?',
                headers=headers, params=payload)
            yield stop.json()
            result = stop.json()
            count +=1


            # assigning values in the dictionary
            for iteration in result["cost_estimates"]:
                if iteration["ride_type"] == "lyft_plus":
                    lyft_plus["min_cost"] += iteration["estimated_cost_cents_min"]
                    lyft_plus["max_cost"] += iteration["estimated_cost_cents_max"]
                    lyft_plus["time"] += iteration["estimated_duration_seconds"]
                    lyft_plus["distance"] += iteration["estimated_distance_miles"]
                    # yield lyft_plus

                elif iteration["ride_type"] == "lyft_line":
                    lyft_line["min_cost"] += iteration["estimated_cost_cents_min"]
                    lyft_line["max_cost"] += iteration["estimated_cost_cents_max"]
                    lyft_line["time"] += iteration["estimated_duration_seconds"]
                    lyft_line["distance"] += iteration["estimated_distance_miles"]
                    # yield lyft_line

                elif iteration["ride_type"] == "lyft":
                    lyft["min_cost"] += iteration["estimated_cost_cents_min"]
                    lyft["max_cost"] += iteration["estimated_cost_cents_max"]
                    lyft["time"] += iteration["estimated_duration_seconds"]
                    lyft["distance"] += iteration["estimated_distance_miles"]
                    # yield lyft

                elif iteration["ride_type"] == "lyft_premier":
                    lyft_premier["min_cost"] = iteration["estimated_cost_cents_min"]
                    lyft_premier["max_cost"] = iteration["estimated_cost_cents_max"]
                    lyft_premier["time"] = iteration["estimated_duration_seconds"]
                    lyft_premier["distance"] = iteration["estimated_distance_miles"]
                    # yield lyft_premier
        cheapest['cost'] = lyft_line['min_cost']
        if(lyft_premier['max_cost']!= 0 and lyft_premier['min_cost']< cheapest['cost']):
            cheapest['cost'] = lyft_premier['min_cost']
            cheapest['time'] = lyft_premier['time']
            cheapest['distance'] = lyft_premier['distance']
            cheapest['type'] = lyft_premier['type']

        if(lyft_plus['max_cost']!= 0 and lyft_plus['min_cost']< cheapest['cost']):
            cheapest['cost'] = lyft_plus['min_cost']
            cheapest['time'] = lyft_plus['time']
            cheapest['distance'] =lyft_plus['distance']
            cheapest['type']= lyft_plus['type']
        if(lyft['max_cost']!= 0 and lyft['min_cost']< cheapest['cost']):
            cheapest['cost'] = lyft['min_cost']
            cheapest['time'] = lyft['time']
            cheapest['distance'] = lyft['distance']
            cheapest['type'] = lyft['type']

        if(lyft_line['min_cost']!= 0 and lyft_premier['min_cost']< cheapest['cost']):
            cheapest['cost'] = lyft_line['min_cost']
            cheapest['time'] = lyft_line['time']
            cheapest['distance'] = lyft_line['distance']
            cheapest['type'] = lyft_line['type']

        yield "FULL TRIP STATISTICS"
        yield "For lyft:",lyft
        yield "For lyft_line:",lyft_line
        yield "For lyft_plus:",lyft_plus
        yield "For lyft_premier:",lyft_premier
        yield 'Cheapest:', cheapest

    # getting details about type of rides for a static location
    @srpc(str,_returns=unicode)
    def getdata(self):
        headers = {
            'Authorization': 'Bearer gAAAAABYOh2rXUfRCrbLM5kt_kICcQvAuyefz_9pJsgGhHQLhKnu3idO-pEgZN6xBWRqXyy0vaOFPse2Rk4i26RCUhKOBvYvnXAW17OwAGpmXdEzG_38O-sYbz9zd_OHdswBrRXFGKy9lBflP0eVWLP3rsCQJd1JuBFJdks2AfawYNAviW1wB2s=',
            'Accept-Language': 'en_US',
            'Content-Type': 'application/json',
        }
        r = requests.get(
            'https://api.lyft.com/v1/ridetypes?lat=37.7833&lng=-122.4167',
            headers=headers)
        return r.json()


    #get charges for a starting and end point
    @srpc(float, float, float, float, _returns=unicode)
    def getcost(startlat, startlon, endlat, endlon):
        global i,total_min_cost, total_max_cost, ride, locationlist
        payload = {'start_lat': startlat, 'start_lng': startlon, 'end_lat': endlat, 'end_lng': endlon}
        headers = {
            'Authorization': 'Bearer gAAAAABYOh2rXUfRCrbLM5kt_kICcQvAuyefz_9pJsgGhHQLhKnu3idO-pEgZN6xBWRqXyy0vaOFPse2Rk4i26RCUhKOBvYvnXAW17OwAGpmXdEzG_38O-sYbz9zd_OHdswBrRXFGKy9lBflP0eVWLP3rsCQJd1JuBFJdks2AfawYNAviW1wB2s=',
            'Accept-Language': 'en_US',
            'Content-Type': 'application/json',
        }

        cost = requests.get(
            'https://api.lyft.com/v1/cost?',
            headers=headers, params=payload)
        yield cost.json()



if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)

    application = Application([Lyft], 'spyne.model.Lyft',
                              in_protocol=HttpRpc(validator='soft'),

                              out_protocol=JsonDocument(ignore_wrappers=True),
                              )
    wsgi_application = WsgiApplication(application)

    server = make_server('127.0.0.1', 5000, wsgi_application)

    logging.info("listening to http://127.0.0.1:5000")
    logging.info("wsdl is at: http://localhost:5000/?wsdl")

server.serve_forever()

