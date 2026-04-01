from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import re

@dataclass
class Bounds:
    minlat: int
    minlon: int
    maxlat: int
    maxlon: int
    
    @classmethod
    def from_dict(cls, d: Optional[Dict[str, float]]) -> Optional['Bounds']:
        if not d: return None
        return cls(**d)
    
@dataclass
class Geometry:
    lat: int
    lon: int
    
    @classmethod
    def from_list(cls, l: Optional[List[Dict[str, float]]]) -> List['Geometry']:
        if not l: return []
        return [cls(lat=pt['lat'], lon=pt['lon']) for pt in l]
    
@dataclass
class MaxSpeed:
    defaultMaxSpeed: int
    bus: Optional[int] = None
    hgv: Optional[int] = None
    
    @classmethod
    def from_dict(cls, tags: Dict[str, str]) -> 'MaxSpeed':
        def extract_int(val: Optional[str]) -> Optional[int]:
            if not val: return None
            match = re.search(r'\d+', str(val))
            return int(match.group()) if match else None

        default = extract_int(tags.get('maxspeed')) or 50
        
        return cls(
            defaultMaxSpeed=default,
            bus=extract_int(tags.get('maxspeed:bus')),
            hgv=extract_int(tags.get('maxspeed:hgv'))
        ) 
    
    
@dataclass
class Tags:
    name: str
    bridge: bool
    highway: str
    designation: str
    lanes: int
    surface: str
    ref: str
    layer: int
    oneway: bool
    hgv_allowed: bool
    maxspeed: MaxSpeed
    maxweight: int
    
    @classmethod
    def from_dict(cls, d: Dict[str, str]) -> 'Tags':
        raw_weight = d.get('maxweight', '-1')
        clean_weight = re.search(r'\d+', str(raw_weight))
        weight_value = int(clean_weight.group()) if clean_weight else -1
        return cls(
            name=d.get('name', 'S/N'),
            bridge=d.get('bridge') == 'yes',
            highway=d.get('highway', 'unclassified'),
            designation=d.get('designation', 'none'),
            lanes=int(d.get('lanes', '1')),
            surface=d.get('surface', 'asphalt'),
            ref=d.get('ref', 'S/R'),
            layer=int(d.get('layer', '0')),
            oneway=d.get('oneway') == 'yes',
            hgv_allowed=d.get('hgv') != 'no',
            maxspeed=MaxSpeed.from_dict(d),
            maxweight=weight_value
        )

@dataclass
class Element:
    type: str
    id: int
    bounds: Bounds
    nodes: List[int]
    geometry: List[Geometry]
    tags: Tags
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Element':
        return cls(
            type=d.get('type', 'way'),
            id=d.get('id', 0),
            tags=Tags.from_dict(d.get('tags', {})),
            bounds=Bounds.from_dict(d.get('bounds')),
            nodes=d.get('nodes', []),
            geometry=Geometry.from_list(d.get('geometry'))
        )
    
    def get_wkt(self) -> Optional[str]:
            if not self.geometry or len(self.geometry) < 2:
                return None
                
            puntos = [f"{g.lon} {g.lat}" for g in self.geometry]
            
            return f"LINESTRING({', '.join(puntos)})"
