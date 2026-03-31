CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgrouting;

[
  { "id": 10, "name": "Costanera Center", "geometry": { "type": "Point", "coordinates": [-70.60661, -33.41722] } },<br>
  { "id": 11, "name": "Metro Tobalaba", "geometry": { "type": "Point", "coordinates": [-70.60123, -33.41850] } },<br>
  { "id": 12, "name": "Parque Bicentenario", "geometry": { "type": "Point", "coordinates": [-70.58752, -33.39821] } },<br>
  { "id": 15, "name": "Plaza Baquedano", "geometry": { "type": "Point", "coordinates": [-70.63450, -33.43720] } },<br>
  { "id": 20, "name": "Cerro San Cristóbal", "geometry": { "type": "Point", "coordinates": [-70.63000, -33.43000] } }<br>
]<br><br>

[
  {
    "id": 1,<br>
    "source": { "id": 12 },<br>
    "target": { "id": 11 },<br>
    "distance": 3200.0,<br>
    "cost": 1500.0,<br>
    "oneway": true,<br>
    "geometry": {
      "type": "LineString",<br>
      "coordinates": [[-70.58752, -33.39821], [-70.60123, -33.41850]]
    }
  },<br>
  {
    "id": 2,<br>
    "source": { "id": 11 },<br>
    "target": { "id": 10 },<br>
    "distance": 850.0,<br>
    "cost": 450.0,<br>
    "oneway": true,<br>
    "geometry": {
      "type": "LineString",<br>
      "coordinates": [[-70.60123, -33.41850], [-70.60661, -33.41722]]
    }
  },<br>
  {
    "id": 3,<br>
    "source": { "id": 10 },<br>
    "target": { "id": 15 },<br>
    "distance": 4500.0,<br>
    "cost": 2100.0,<br>
    "oneway": true,<br>
    "geometry": {
      "type": "LineString",<br>
      "coordinates": [[-70.60661, -33.41722], [-70.62000, -33.42500], [-70.63450, -33.43720]]
    }
  }
]<br><br>

http://localhost:8000/api/edge/v1/route?sourceNodeId=12&targetNodeId=15<br>