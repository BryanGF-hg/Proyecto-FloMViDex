import json
import pymysql
import os

# Como este script está en la carpeta 'backend', la ruta a 'data' es relativa y directa!
JSON_PATH = os.path.join("data", "tracks.json")

def migrar_json_a_sql():
    print("Iniciando la migración de datos...")
    # 1. Leer el archivo JSON Maestro (tracks.json)
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            db_json = json.load(f)
        print(f"✅ Archivo JSON '{JSON_PATH}' cargado correctamente.")
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo JSON en la ruta: {JSON_PATH}")
        return
    except json.JSONDecodeError:
        print("❌ Error: El archivo tracks.json tiene un formato inválido o está corrupto.")
        return

    # 2. Conectar a MySQL
    try:
        conexion = pymysql.connect(
            host='localhost',
            user='dj_maidcore',
            password='dj_maidcore',
            database='flomvidex'
        )
        cursor = conexion.cursor()
        print("✅ Conectado a la base de datos MySQL 'flomvidex'.")
    except Exception as e:
        print(f"❌ Error al conectar a MySQL. ¿Está encendido el servidor? Detalles: {e}")
        return

    # 3. Procesar e Insertar los datos
    tracks_insertados = 0
    
    try:
        # Recorremos los 4 arrays (mc1, mc2, mc3, mc4)
        for directorio, lista_canciones in db_json.items():
            print(f"Procesando directorio: {directorio}...")
            
            for track in lista_canciones:
                # Extrae datos de forma segura (por si falta algún campo)
                title = track.get("title", "")
                file = track.get("file", "")
                artist = track.get("artist", "")
                dir_name = track.get("dir", directorio) # Usamos el del JSON, o la llave base (ej: mc1)
                
                # Convertir los tags (que son un Array en JSON) a un String separado por comas para SQL
                tags_raw = track.get("tags", [])
                tags_str = ",".join(tags_raw) if isinstance(tags_raw, list) else str(tags_raw)
#####################################################
                # ATENCIÓN: No insertamos el 'id' del JSON. 
                # Dejamos que MySQL asigne un ID único global autoincremental para evitar choques entre mc1 y mc2.
#####################################################                
                sql = """
                    INSERT INTO tracks (title, file, artist, tags, dir) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (title, file, artist, tags_str, dir_name))
                tracks_insertados += 1
        
        # Confirmar los cambios en la base de datos
        conexion.commit()
        print(f" ¡Migración exitosa! Se insertaron {tracks_insertados} canciones en total.")
        
        # Guardar un registro de la acción en la tabla 'logs'
        log_sql = "INSERT INTO logs (action) VALUES (%s)"
        cursor.execute(log_sql, (f"Migración inicial: {tracks_insertados} tracks importados desde JSON",))
        conexion.commit()

    except Exception as e:
        # Si algo falla, revertimos los cambios para no dejar la base de datos a medias
        conexion.rollback()
        print(f"❌ Error crítico durante la inserción SQL: {e}")
        print("Se han revertido los cambios.")
    finally:
        cursor.close()
        conexion.close()
        print("🔌 Conexión a MySQL cerrada.")

if __name__ == "__main__":
    migrar_json_a_sql()
