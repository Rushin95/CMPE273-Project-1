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
    i = 0
    total_min_cost = 0.0
    total_max_cost = 0.0
    ride = 0
    global l
    locationlist = []

    # set source location
    @srpc(str,float, float, _returns=unicode)
    def setsource(self,sourcelat,sourcelon):

        # payload = {'lat': sourcelat, 'lng': sourcelon}
        # headers = {
        #     'Authorization': 'Bearer gAAAAABYOh2rXUfRCrbLM5kt_kICcQvAuyefz_9pJsgGhHQLhKnu3idO-pEgZN6xBWRqXyy0vaOFPse2Rk4i26RCUhKOBvYvnXAW17OwAGpmXdEzG_38O-sYbz9zd_OHdswBrRXFGKy9lBflP0eVWLP3rsCQJd1JuBFJdks2AfawYNAviW1wB2s=',
        #     'Accept-Language': 'en_US',
        #     'Content-Type': 'application/json',
        # }
        #
        # source = requests.get(
        #     'https://api.lyft.com/v1/setsource?',
        #     headers=headers, params=payload)
        locationlist.append((sourcelat, sourcelon))
        # yield source.json()
        yield "source:",locationlist[0]

        # set destination location
    @srpc(str,float, float, _returns=unicode)
    def setdestination(self,destinationlat, destinationlon):

        # payload = {'lat': destinationlon, 'lng': destinationlon}
        # headers = {
        #     'Authorization': 'Bearer gAAAAABYOh2rXUfRCrbLM5kt_kICcQvAuyefz_9pJsgGhHQLhKnu3idO-pEgZN6xBWRqXyy0vaOFPse2Rk4i26RCUhKOBvYvnXAW17OwAGpmXdEzG_38O-sYbz9zd_OHdswBrRXFGKy9lBflP0eVWLP3rsCQJd1JuBFJdks2AfawYNAviW1wB2s=',
        #     'Accept-Language': 'en_US',
        #     'Content-Type': 'application/json',
        # }
        #
        # source = requests.get(
        #     'https://api.lyft.com/v1/setsource?',
        #     headers=headers, params=payload)

        # set destination coordinates as last element of array
        locationlist.append((destinationlat, destinationlon))
        l = len(locationlist)
        # yield source.json()
        yield "num:",l-1, " destination:", locationlist[l-1]
        yield locationlist[l - 1]

    # getting details about type of rides for static location
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



    # add location
    @srpc(float, float,int, _returns=unicode)
    def addlocation(lat,lon,num):
        global total_min_cost, total_max_cost, locationlist

        # payload = {'start_lat': startlat, 'start_lng': startlon, 'end_lat': endlat, 'end_lng': endlon}
        # headers = {
        #     'Authorization': 'Bearer gAAAAABYOh2rXUfRCrbLM5kt_kICcQvAuyefz_9pJsgGhHQLhKnu3idO-pEgZN6xBWRqXyy0vaOFPse2Rk4i26RCUhKOBvYvnXAW17OwAGpmXdEzG_38O-sYbz9zd_OHdswBrRXFGKy9lBflP0eVWLP3rsCQJd1JuBFJdks2AfawYNAviW1wB2s=',
        #     'Accept-Language': 'en_US',
        #     'Content-Type': 'application/json',
        # }
        #
        # cost = requests.get(
        #     'https://api.lyft.com/v1/cost?',
        #     headers=headers, params=payload)
        # yield cost.json()
        #
        #
        #
        # stop = cost.json()
        #
        # total_min_cost += stop["cost_estimates"][0]["estimated_cost_cents_min"]
        # yield "Total minimum cost :", total_min_cost
        #
        # total_max_cost += stop["cost_estimates"][0]["estimated_cost_cents_max"]
        # yield "Total maximum cost :", total_max_cost

        # add location to the list
        locationlist[num] = (lat,lon)
        yield "num:",num,"source:",locationlist[0], "this location:" , locationlist[num]

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

