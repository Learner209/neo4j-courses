import unittest
import requests


class TestCRUDOperations(unittest.TestCase):
    base_url = "http://127.0.0.1:8000"
    example_course = "CS1604"

    def test_create_node(self):
        params = {
            "alias": "os_concepts",
            "node_type": "INTERRUPT",
            "properties": {"context": "thread", "os": "linux"},
        }
        response = requests.get(
            f"{self.base_url}/create/entities/{self.example_course}", json=params
        )
        self.assertEqual(response.status_code, 200)

    def test_update_node(self):
        params = {
            "identifying_property": "debugging",
            "new_properties": {"utils": "gdb"},
            "node_type": "Entity",
        }
        response = requests.get(
            f"{self.base_url}/update/entities/{self.example_course}", json=params
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_node(self):
        params = {"node_type": "Entity", "identifying_property": "debugging"}
        response = requests.get(
            f"{self.base_url}/delete/entities/{self.example_course}", json=params
        )
        self.assertEqual(response.status_code, 200)

    def test_create_rel(self):
        params = {
            "node_type1": "Entity",
            "node_type2": "Entity",
            "name1": "StanfordCppLib",
            "name2": "Queue",
            "rel_type": "USES",
            "properties": {"method": "exclusive"},
        }
        response = requests.get(
            f"{self.base_url}/create/rel/{self.example_course}", json=params
        )
        self.assertEqual(response.status_code, 200)

    def test_update_rel(self):
        params = {
            "name1": "mingw32-make",
            "name2": "Makefile linux",
            "rel_type": "RELATED_TO",
            "new_properties": {"method": "shared"},
        }
        response = requests.get(
            f"{self.base_url}/update/rel/{self.example_course}", json=params
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_rel(self):
        params = {
            "rel_type": "RELATED_TO",
            "name1": "mingw32-make",
            "name2": "Makefile linux",
        }
        response = requests.get(
            f"{self.base_url}/delete/rel/{self.example_course}", json=params
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
