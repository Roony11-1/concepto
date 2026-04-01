import json
import psycopg2
from psycopg2 import extras
from psycopg2.extensions import cursor as PsycopgCursor
from typing import List
import re
import os

from Element import Element

# 1. Configuración de la base de datos
DB_CONFIG = {
    "dbname": "db_rutas",
    "user": "admin",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}

"""
[out:json][timeout:300];

area["name"~"^(Cerrillos|La Reina|Pudahuel|Cerro Navia|Las Condes|Quilicura|Conchalí|Lo Barnechea|Quinta Normal|El Bosque|Lo Espejo|Recoleta|Estación Central|Lo Prado|Renca|Huechuraba|Macul|San Miguel|Independencia|Maipú|San Joaquín|La Cisterna|Ñuñoa|San Ramón|La Florida|Pedro Aguirre Cerda|Santiago|La Pintana|Peñalolén|Vitacura|La Granja|Providencia|Puente Alto)$"]["admin_level"="8"]->.comunas;

(
  way["highway"~"^(motorway|trunk|primary|secondary|tertiary|unclassified|residential)$"]
     ["access"!~"private|no"]
     ["surface"~"asphalt|paved|concrete"]
     (area.comunas);
);

/* 'out geom' incluye la lat/lon dentro de cada 'way'.
  Esto evita tener que buscar nodos por ID en el script.
*/
out geom;
"""

def clean_numeric(value) -> int | None:
    """Extrae solo los números de un string (útil para maxspeed o maxweight)"""
    if value is None:
        return None
    numbers = re.findall(r'\d+', str(value))
    return int(numbers[0]) if numbers else None

def create_edge_table(cur: PsycopgCursor) -> None:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS edge (
            id SERIAL PRIMARY KEY,
            element_id BIGINT UNIQUE,          -- ID original de OSM
            name TEXT,                   -- Nombre de la calle
            highway TEXT,                -- Tipo (motorway, residential, etc.)
            surface TEXT,                -- Superficie (asphalt, concrete)
            lanes INTEGER,               -- Cantidad de pistas
            maxspeed INTEGER,            -- Velocidad máxima
            maxspeed_bus INTEGER,
            maxspeed_hgv INTEGER,
            maxweight FLOAT,             -- Restricción de peso
            oneway INTEGER,              -- 1=Sentido único, 0=Doble sentido
            geometry GEOMETRY(LineString, 4326),
            source INTEGER,              -- Nodo inicial (llenado por pgr_createTopology)
            target INTEGER,              -- Nodo final (llenado por pgr_createTopology)
            cost FLOAT8,                 -- Costo de ida (longitud o tiempo)
            reverse_cost FLOAT8          -- Costo de vuelta (-1 si es oneway)
        );

        -- Índice espacial GIST: Vital para que las búsquedas geográficas sean rápidas
        CREATE INDEX IF NOT EXISTS edge_gix ON edge USING GIST (geometry);
        
        -- Índice en element_id: Acelera el ON CONFLICT durante la carga masiva
        CREATE INDEX IF NOT EXISTS edge_id2_idx ON edge (element_id);
    """)
    print("Tabla e índices listos.")
    
def insert_elements_into_edge(cur: PsycopgCursor, elementos: List[Element]) -> None:
    query = """
    INSERT INTO edge (
        element_id, name, highway, surface, 
        lanes, maxspeed, maxspeed_bus, maxspeed_hgv, 
        maxweight, oneway, geometry
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))
    ON CONFLICT (element_id) DO NOTHING;
    """
    
    data_to_insert = [
        (
            e.id,
            e.tags.name,
            e.tags.highway,
            e.tags.surface,
            e.tags.lanes,
            e.tags.maxspeed.defaultMaxSpeed,
            e.tags.maxspeed.bus or e.tags.maxspeed.defaultMaxSpeed,
            e.tags.maxspeed.hgv or e.tags.maxspeed.defaultMaxSpeed,
            e.tags.maxweight,
            1 if e.tags.oneway else 0,
            e.get_wkt()
        )
        
        for e in elementos
    ]

    try:
        extras.execute_batch(cur, query, data_to_insert, page_size=100)
        print(f"Inserción masiva completada: {len(data_to_insert)} vías procesadas.")
    except Exception as err:
        print(f"Error en la inserción masiva: {err}")

def load_osm_to_postgres(json_file):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("--- Conexión establecida con éxito ---")

        create_edge_table(cur)

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        raw_elements = [e for e in data.get('elements', []) if e['type'] == 'way']
        print(f"Procesando {len(raw_elements)} vías...")
        
        elements: List[Element] = []
        
        for element in raw_elements:
            try:
                e = Element.from_dict(element)
                
                if not e.get_wkt():
                    continue
                
                elements.append(e)
            except Exception as err:
                osm_id = element.get('id', 'Desconocido')
                print(f"Error al procesar la vía id: {osm_id} - {err}")

        insert_elements_into_edge(cur, elements)
        
        conn.commit()
        print(f"--- Carga finalizada: {len(elements)} registros nuevos en 'edge' ---")

    except Exception as e:
        print(f"Error crítico durante la carga: {e}")
        if conn: conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    folder = os.path.dirname(os.path.abspath(__file__))
    path_to_json = os.path.join(folder, 'export.json')
    
    load_osm_to_postgres(path_to_json)