import unittest
import requests


class TestCRUDOperations(unittest.TestCase):
    base_url = "http://127.0.0.1:8000"
    example_course = "CS1604"

    def test_create_node(self):
        params = {
            "name": "INTERRUPT",  # node的名字:只在创建过程中使用到,之后就无法获得了.
            "properties": {
                "context": "thread",
                "os": "linux",
            },  # node的属性,描述node的特征,可以用来进行匹配,查询等操作.
        }
        response = requests.get(
            f"{self.base_url}/create/entities/{self.example_course}", json=params
        )
        self.assertEqual(response.status_code, 200)

    def test_update_node(self):
        params = {
            "name": "debugging",  # 用来匹配待更新节点的名字
            "new_properties": {
                "utils": "gdb"
            },  # 更新节点的新的属性,作为键值对的形式存在.
        }
        response = requests.get(
            f"{self.base_url}/update/entities/{self.example_course}", json=params
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_node(self):
        params = {"name": "debugging"}  # 用来匹配待删除节点的名字
        response = requests.get(
            f"{self.base_url}/delete/entities/{self.example_course}", json=params
        )
        self.assertEqual(response.status_code, 200)

    def test_create_rel(self):
        params = {
            "name1": "StanfordCppLib",  # 用来匹配起始节点的名字
            "name2": "Queue",  # 用来匹配终点节点的名字
            "rel_type": "USES",  # 用来匹配连接起始节点和终点节点的关系的名字
            "properties": {
                "method": "exclusive"
            },  # 新创建关系的属性,作为键值对的形式存在.
        }
        response = requests.get(
            f"{self.base_url}/create/rel/{self.example_course}", json=params
        )
        self.assertEqual(response.status_code, 200)

    def test_update_rel(self):
        params = {
            "name1": "mingw32-make",  # 用来匹配起始节点的名字
            "name2": "Makefile linux",  # 用来匹配终点节点的名字
            "rel_type": "RELATED_TO",  # 用来匹配连接起始节点和终点节点的关系的名字
            "new_properties": {
                "method": "shared"
            },  # 更新关系的新的属性,作为键值对的形式存在.
        }
        response = requests.get(
            f"{self.base_url}/update/rel/{self.example_course}", json=params
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_rel(self):
        params = {
            "rel_type": "RELATED_TO",  # 用来匹配待删除关系的名字
            "name1": "mingw32-make",  # 用来匹配起始节点的名字
            "name2": "Makefile linux",  # 用来匹配终点节点的名字
        }
        response = requests.get(
            f"{self.base_url}/delete/rel/{self.example_course}", json=params
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
