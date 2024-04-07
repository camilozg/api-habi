import configparser
import json
from contextlib import suppress
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

import mysql.connector

# Leer el archivo de condfiguraición config.ini
config = configparser.ConfigParser()
config.read("./config.ini")

# Establecer variables para la conexion a la base de datos
DB_HOST = config.get("database", "host")
DB_PORT = config.get("database", "port")
DB_USER = config.get("database", "user")
DB_PASSWORD = config.get("database", "password")
DB_SCHEMA = config.get("database", "schema")


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Procesar la URL de la petición para poder acceder a sus distindos componentes
        parsed_url = urlparse(self.path)

        # Validar que la petición sea realizada al endpoint "/api/property"
        if parsed_url.path == "/api/property":
            # Recuperar los parámetros de la petición GET para los filtros año, ciudad y estado
            query = parsed_url.query
            params = dict(param.split("=") for param in query.split("&")) if query else {}

            try:
                # Realizar la conexión a la base de datos
                conn = mysql.connector.connect(
                    host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_SCHEMA
                )

                # Generar un cursor para ejecutar búsquedas parametrizadas
                cursor = conn.cursor(prepared=True)

                # Sentencia SQL para la extracción de inmuebles
                stmt = """
                            select distinct
                                p.address,
                                p.city,
                                p.year,
                                s.name as status,
                                p.price,
                                p.description
                            from
                                property p
                            left join ( select property_id, max(update_date) as max_date
                                        from status_history sh
                                        group by property_id ) d
                                on  p.id = d.property_id
                            left join status_history sh
                                on p.id = sh.property_id
                                and d.max_date = sh.update_date
                            left join status s
                                on sh.status_id = s.id
                            where
                                p.address is not null
                                and p.address <> ''
                                and s.id in (3, 4, 5)
                        """

                # Modificar la sentencia SQL con base en los parámetros de la petición GET
                params_list = []
                if "city" in params:
                    stmt += " AND city = %s"
                    params_list.append(params["city"])
                if "year" in params:
                    stmt += " AND year = %s"
                    params_list.append(params["year"])
                if "status" in params:
                    stmt += " AND s.name = %s"
                    params_list.append(params["status"])

                # Ejecutar la sentencia con los parámetros de filtrado y obtener el resultado
                cursor.execute(stmt, tuple(params_list))
                result = cursor.fetchall()

                # Generar un diccionario con el resultado de la consulta y los nombres de los atributos
                result_dict = []
                columns = ("address", "city", "year", "status", "price", "description")
                for row in result:
                    result_dict.append(dict(zip(columns, row)))

                # Enviar el código de respuesta, encabezado y el contenido en formato JSON
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result_dict).encode("utf-8"))

            except mysql.connector.Error:
                # Enviar el código "500 Internal Server Error" si falla la conexión a la base de datos
                self.send_response(500)

            finally:
                # Cierra la conexión a la base de datos en caso de que exista
                with suppress(NameError):
                    if conn.is_connected():
                        cursor.close()
                        conn.close()
        else:
            # Enviar el código "403 Forbidden" si la peticiín no se realiza al endpoint especificado
            self.send_response(403)


if __name__ == "__main__":
    # Instancia del servidor HTTP
    server = HTTPServer(("localhost", 8000), HTTPRequestHandler)
    try:
        # Ejecutar el servidor
        print("Starting server...")
        server.serve_forever()
    except KeyboardInterrupt:
        # Detener el servidor con la interrupción por teclado "Ctrl + C"
        print("Stopping server...")
        server.server_close()
