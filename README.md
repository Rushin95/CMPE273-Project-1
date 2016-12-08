# CMPE273-Project
Final Project CMPE273 class

##############Installation##############
1. Clone it or download the file on your system.
2. Install and import all project requirements as mentioned in requirements.txt file.
3. Change the DB_PASSWORD as your database password in:
   Instance->config.py
4. Make run.py as the starting poin.
You're good to go then.
########################################
### Algorithm
1. We've implemented our own version of algorithm from Travelling salseman probelm and Dijkstra's algorithm.
2. We're calculating best route based on the price.
3. Starting with comparing price of 1st value with each and every middle points, selecting the route which is taking the least cost.
4. Then taking that travesed point and calculating with others in a loop and making our best optimized route in dynamic way.
########################################
# Calculation
After finding optmized path
1. We're calling uber and lyft API's to calculate price of available transport type like Uber X, Uber XL, Uber Select, Lyft, Lyft Plus etc.
2. Implemented and transformed google maps path draw function, to draw our calculated optimized path and show it as result.
####################

As this is our first iteration of delivery, we tried to do error handling. It might wont work for some extream cases, but we tried to do our best.

## 2. Trip Planner using Uber vs Lyft's Price Estimation

### Requirement

* Plan a trip which consists of a set of places and estimate the total cost between Uber and Lyft.
* You need to store location details and price estimate data into a persistent DB.
* FEEL FREE TO ADD ANY APIS THAT YOU NEED.

#### I. Location APIs

* 1. Create Location: POST /locations

> Call Google Map API to look up coordinates. http://maps.google.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&sensor=false

__Request__

```json
{
   "name" : "My Home",
   "address" : "123 Main St",
   "city" : "San Francisco",
   "state" : "CA",
   "zip" : "94113"
}
```

__Response__

```json
{
   "id" : 12345,
   "name" : "My Home",
   "address" : "123 Main St",
   "city" : "San Francisco",
   "state" : "CA",
   "zip" : "94113",
   "coordinate" : {
      "lat" : 38.4220352,
      "lng" : -222.0841244
   }
}
```

* 2. Get a location: GET /locations/12345

__Response__

```json
{
   "id" : 12345,
   "name" : "My Home",
   "address" : "123 Main St",
   "city" : "San Francisco",
   "state" : "CA",
   "zip" : "94113",
   "coordinate" : {
      "lat" : 38.4220352,
      "lng" : -222.0841244
   }
}
```

* 3. Update a location: PUT /locations/12345

__Request__

```json
{
   "name" : "My New Home"
}
```

* 4. Delete a location: DELETE /locations/12345

#### II. Trip Planner APIs

* 1. Plan a trip: POST /trips

__Request__

```json
{
    "start": "/locations/12345",
    "others" : [
        "/locations/1000",
        "/locations/1001",
        "/locations/1002",
    ],
    "end": "/locations/12345"
}
```

__Response__

```json
{
    "id": 200000,
    "start": "/locations/12345",
    "best_route_by_costs" : [
        "/locations/1002",
        "/locations/1000",
        "/locations/1001",
    ],
    "providers" : [
        {
            "name" : "Uber",
            "total_costs_by_cheapest_car_type" : 125,
            "currency_code": "USD",
            "total_duration" : 640,
            "duration_unit": "minute",
            "total_distance" : 25.05,
            "distance_unit": "mile"
        },
        {
            "name" : "Lyft",
            "total_costs_by_cheapest_car_type" : 110,
            "currency_code": "USD",
            "total_duration" : 620,
            "duration_unit": "minute",
            "total_distance" : 25.05,
            "distance_unit": "mile"
        }
    ],
    "end": "/locations/12345"
}
```

### Dependency

- [Lyft Pricing API](https://developer.lyft.com/docs/availability-cost)
- [Uber Pricing API](https://developer.uber.com/docs/ride-requests/references/api/v1-estimates-price-get)
