from fastapi import FastAPI
import httpx
import polyline
from typing import List, Dict, Any, Optional

app = FastAPI()


class TransitApi:
    """General client following GTFS transit data format to supply data about a city's transit network"""

    def __init__(self, API_url):
        self.API=API_url





class MBTAApiClient:
    """Client to interact with MBTA v3 API"""
    
    BASE_URL = "https://api-v3.mbta.com"
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_routes(self) -> List[Dict[str, Any]]:
        """Get all routes from MBTA API"""
        try:
            response = await self.client.get(f"{self.BASE_URL}/routes", params={
                "page[limit]": 100
            })
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            print(f"Error fetching routes: {e}")
            return []
    
    async def get_stops_for_route(self, route_id: str) -> List[Dict[str, Any]]:
        """Get stops for a specific route"""
        try:
            response = await self.client.get(f"{self.BASE_URL}/stops", params={
                "filter[route]": route_id,
                "page[limit]": 100
            })
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            print(f"Error fetching stops for route {route_id}: {e}")
            return []
    
    async def get_shapes_for_route(self, route_id: str) -> List[Dict[str, Any]]:
        """Get shapes (coordinates) for a specific route"""
        try:
            # Get shapes for the route
            response = await self.client.get(f"{self.BASE_URL}/shapes", params={
                "filter[route]": route_id,
                "page[limit]": 100
            })
            response.raise_for_status()
            data = response.json()
            
            # Process the shapes to extract coordinates from polylines
            shapes = []
            for item in data.get("data", []):
                attributes = item.get("attributes", {})
                polyline_str = attributes.get("polyline")
                
                # Decode the polyline to get coordinates
                points = []
                if polyline_str:
                    try:
                        decoded_coords = polyline.decode(polyline_str)
                        # Convert to Leaflet format [lat, lng]
                        points = [[coord[1], coord[0]] for coord in decoded_coords]
                    except Exception as e:
                        print(f"Error decoding polyline for shape {item.get('id')}: {e}")
                
                shapes.append({
                    "id": item.get("id"),
                    "direction_id": attributes.get("direction_id"),
                    "points": points,
                    "priority": attributes.get("priority"),
                    "shape_dist_traveled": attributes.get("shape_dist_traveled")
                })
            
            return shapes
        except Exception as e:
            print(f"Error fetching shapes for route {route_id}: {e}")
            return []
    
    async def get_predictions_and_vehicles(self, route_id: str) -> Dict[str, Any]:
        """Get real-time vehicle positions for a route"""
        try:
            response = await self.client.get(f"{self.BASE_URL}/vehicles", params={
                "filter[route]": route_id,
                "include": "stop,trip"
            })
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching vehicles for route {route_id}: {e}")
            return {}
    
    async def close(self):
        await self.client.aclose()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api/mbta/routes")
async def get_mbta_routes():
    """Get all MBTA routes (trains, buses, etc.) with basic information"""
    client = MBTAApiClient()
    try:
        routes = await client.get_routes()
        
        # Format the routes for frontend consumption
        formatted_routes = []
        for route in routes:
            route_attrs = route.get("attributes", {})
            formatted_routes.append({
                "id": route.get("id"),
                "type": route_attrs.get("type"),
                "name": route_attrs.get("long_name") or route_attrs.get("short_name", ""),
                "color": route_attrs.get("color"),
                "text_color": route_attrs.get("text_color"),
                "description": route_attrs.get("description"),
                "direction_names": route_attrs.get("direction_names", []),
                "direction_destinations": route_attrs.get("direction_destinations", [])
            })
        
        return {"routes": formatted_routes}
    finally:
        await client.close()


@app.get("/api/mbta/route/{route_id}/shapes")
async def get_mbta_route_shapes(route_id: str):
    """Get shape coordinates for a specific route to draw on the map"""
    client = MBTAApiClient()
    try:
        shapes = await client.get_shapes_for_route(route_id)
        
        return {"route_id": route_id, "shapes": shapes}
    finally:
        await client.close()


@app.get("/api/mbta/route/{route_id}/stops")
async def get_mbta_route_stops(route_id: str):
    """Get stops for a specific route"""
    client = MBTAApiClient()
    try:
        stops = await client.get_stops_for_route(route_id)
        
        formatted_stops = []
        for stop in stops:
            stop_attrs = stop.get("attributes", {})
            location_type = stop_attrs.get("location_type", 0)
            
            formatted_stops.append({
                "id": stop.get("id"),
                "name": stop_attrs.get("name"),
                "latitude": stop_attrs.get("latitude"),
                "longitude": stop_attrs.get("longitude"),
                "location_type": location_type,  # 0=stop, 1=station
                "wheelchair_boarding": stop_attrs.get("wheelchair_boarding"),
                "description": stop_attrs.get("description")
            })
        
        return {"route_id": route_id, "stops": formatted_stops}
    finally:
        await client.close()


@app.get("/api/mbta/transit-data")
async def get_complete_transit_data():
    """Get comprehensive transit data for all routes with shapes and stops"""
    client = MBTAApiClient()
    try:
        routes = await client.get_routes()
        
        transit_data = {
            "routes": [],
            "shapes": {},
            "stops": {}
        }
        
        for route in routes:
            route_attrs = route.get("attributes", {})
            route_type = route_attrs.get("type")
            
            # Filter for subway, light rail, and bus routes only (types 0, 1, 2, 3)
            # 0: Light rail, 1: Subway, 2: Rail, 3: Bus
            if route_type in [0, 1, 2, 3]:
                route_info = {
                    "id": route.get("id"),
                    "type": route_type,
                    "name": route_attrs.get("long_name") or route_attrs.get("short_name", ""),
                    "color": route_attrs.get("color"),
                    "text_color": route_attrs.get("text_color"),
                    "description": route_attrs.get("description")
                }
                transit_data["routes"].append(route_info)
                
                # Get shapes for this route
                shapes = await client.get_shapes_for_route(route.get("id"))
                transit_data["shapes"][route.get("id")] = shapes
                
                # Get stops for this route
                stops = await client.get_stops_for_route(route.get("id"))
                route_stops = []
                for stop in stops:
                    stop_attrs = stop.get("attributes", {})
                    route_stops.append({
                        "id": stop.get("id"),
                        "name": stop_attrs.get("name"),
                        "latitude": stop_attrs.get("latitude"),
                        "longitude": stop_attrs.get("longitude")
                    })
                
                transit_data["stops"][route.get("id")] = route_stops
        
        return transit_data
    finally:
        await client.close()


@app.get("/api/mbta/vehicles/{route_id}")
async def get_mbta_vehicles(route_id: str):
    """Get real-time vehicle positions for a specific route"""
    client = MBTAApiClient()
    try:
        response = await client.get_predictions_and_vehicles(route_id)
        return response
    finally:
        await client.close()