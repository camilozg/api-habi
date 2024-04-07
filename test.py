import requests

# URL del endpoint
URL = "http://localhost:8000/api/property"


class TestClass:
    @staticmethod
    def send_request(params=None):
        """Permite enviar las peticiones de búsqueda de inmuebles al API y hace
        validaciones genéricas, retornando la data recuperada en la respuesta."""

        response = requests.get(URL, params)
        data = response.json()
        assert response.status_code == 200
        assert len(data) > 0

        return data

    def test_search_without_any_filter(self):
        self.send_request()

    def test_fetch_properties_with_allowed_status_only(self):
        allowed_status = ("pre_venta", "en_venta", "vendido")
        data = self.send_request()
        assert all(p["status"] in allowed_status for p in data)

    def test_search_by_year(self):
        params = {"year": 2020}
        data = self.send_request(params)
        assert all(p["year"] == params["year"] for p in data)

    def test_search_by_city(self):
        params = {"city": "bogota"}
        data = self.send_request(params)
        assert all(p["city"] == params["city"] for p in data)

    def test_search_by_status(self):
        params = {"status": "en_venta"}
        data = self.send_request(params)
        assert all(p["status"] == params["status"] for p in data)

    def test_search_by_year_and_city(self):
        params = {"year": 2002, "city": "medellin"}
        data = self.send_request(params)
        assert all(p["year"] == params["year"] and p["city"] == params["city"] for p in data)

    def test_search_by_year_and_status(self):
        params = {"year": 2011, "status": "en_venta"}
        data = self.send_request(params)
        assert all(p["year"] == params["year"] and p["status"] == params["status"] for p in data)

    def test_search_by_city_and_status(self):
        params = {"city": "barranquilla", "status": "vendido"}
        data = self.send_request(params)
        assert all(p["city"] == params["city"] and p["status"] == params["status"] for p in data)

    def test_search_with_all_filter(self):
        params = {"year": 2021, "city": "pereira", "status": "pre_venta"}
        data = self.send_request(params)
        assert all(
            p["year"] == params["year"] and p["city"] == params["city"] and p["status"] == params["status"]
            for p in data
        )
