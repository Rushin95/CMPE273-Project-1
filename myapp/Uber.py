# ---------------------------------------------------------------------------

import datetime
import logging
import time

import requests
from spyne.application import Application
from spyne.decorator import srpc
from spyne.model.complex import Iterable
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
from spyne.service import ServiceBase

class Uber(ServiceBase):
    @srpc(str,_returns=unicode)
    def getdata(self):
        headers = {
            'Authorization': 'Token aTS7ifSRpVChp5-VsDkVxTrlZyUSA9g2qdH81E2k',
            'Accept-Language': 'en_US',
            'Content-Type': 'application/json',
        }
        coordsA = {'lat':'37.334762', 'lon':'-121.907705'}
        URL="https://api.uber.com/v1.2/estimates/price"
        para1 = {'start_latitude':'37.334762','start_longitude':'-121.907705','end_latitude':'37.335532','end_longitude':'-121.885476'}
        para2=  {'start_latitude':'37.335532','start_longitude':'-121.885476','end_latitude':'37.413477','end_longitude':'-121.898105'}
        para3=  {'start_latitude':'37.413477','start_longitude':'-121.898105','end_latitude':'37.383757','end_longitude':'-121.886364'}
        r1 = requests.get(URL,params=para1,headers=headers)
        r2 = requests.get(URL,params=para2,headers=headers)
        r3 = requests.get(URL,params=para3,headers=headers)
        data1=r1.json()
        intA=data1["prices"][1]["estimate"]
        addA = intA.split("$")[-1]
        a1=addA.split("-")[0]#First Value
        a1=int(a1)
        a2=addA.split("-")[-1]#Second Value
        a2=int(a2)
        data2=r2.json()
        intB=data2["prices"][1]["estimate"]
        addB = intB.split("$")[-1]
        b1=addB.split("-")[0]#First Value
        b1=int(b1)
        b2=addB.split("-")[-1]#Second Value
        b2=int(b2)
        data3=r3.json()
        intC=data3["prices"][1]["estimate"]
        addC = intC.split("$")[-1]
        c1=addC.split("-")[0]#First Value
        c1=int(c1)
        c2=addC.split("-")[-1]#Second Value
        c2=int(c2)
        first=a1+b1+c1
        second=a2+b2+c2
        print1= "Total Estimated Price :"+str(first)+","+str(second)
        #return (coordsA.get('lat'))
        return (print1)

if __name__ == '__main__':
    # Python daemon boilerplate
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)

    # Instantiate the application by giving it:
    #   * The list of services it should wrap,
    #   * A namespace string.
    #   * An input protocol.
    #   * An output protocol.
    application = Application([Uber], 'spyne.model.Uber',
                              # The input protocol is set as HttpRpc to make our service easy to
                              # call. Input validation via the 'soft' engine is enabled. (which is
                              # actually the the only validation method for HttpRpc.)
                              in_protocol=HttpRpc(validator='soft'),

                              # The ignore_wrappers parameter to JsonDocument simplifies the reponse
                              # dict by skipping outer response structures that are redundant when
                              # the client knows what object to expect.
                              out_protocol=JsonDocument(ignore_wrappers=True),
                              )

    # Now that we have our application, we must wrap it inside a transport.
    # In this case, we use Spyne's standard Wsgi wrapper. Spyne supports
    # popular Http wrappers like Twisted, Django, Pyramid, etc. as well as
    # a ZeroMQ (REQ/REP) wrapper.
    wsgi_application = WsgiApplication(application)

    # More daemon boilerplate
    server = make_server('127.0.0.1', 5000, wsgi_application)

    logging.info("listening to http://127.0.0.1:5000")
    logging.info("wsdl is at: http://localhost:5000/?wsdl")

server.serve_forever()