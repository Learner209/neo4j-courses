# Neo4j 知识图谱系统 API 文档:

## 1. 端点: `/dag/courses/`

- **描述**：在 Neo4j 数据库中搜索处于先修课程数据库的课程实体。
- **方法**：`GET`
- **参数**： 无
- **返回**：返回每个课程实体的学分,学时,课程编号,课程名称
- **请求示例**：`GET /dag/courses/`
- **响应示例**：
  ```json
  [
     {
    "hours": 64,
    "name": "计算导论",
    "code": "CS1602",
    "credits": 4
  },
  {
    "hours": 64,
    "name": "程序设计原理与方法",
    "code": "CS1604",
    "credits": 4
  }, ...
  ]
    ```   

## 2. 端点: `/dag/rels/`

- **描述**：在 Neo4j 数据库中搜索处于先修课程数据库的课程关系。
- **方法**：`GET`
- **参数**： 无
- **返回**：返回每个课程先修关系中的先修课程,后修课程和关系名称(指定为`PREREQUISITE FOR`)
- **请求示例**：`GET /dag/rels/`
- **响应示例**：
  ```json
  [
  {
    "prerequisite": {
      "hours": 8,
      "code": "MARX1 205",
      "credits": 0.5,
      "name": "形势与政策"
    },
    "end": {
      "hours": 32,
      "code": "MIL120 1",
      "credits": 2,
      "name": "军事理论"
    },
    "rel": [
      {
        "hours": 8,
        "code": "MARX1 205",
        "credits": 0.5,
        "name": "形势与政策"
      },
      "PREREQUISITE_FOR",
      {
        "hours": 32,
        "code": "MIL120 1",
        "credits": 2,
        "name": "军事理论"
      }
    ]
  },...
  ]
    ```

## 3. 端点: `/course/entities/{title}`

- **描述**：在 Neo4j 数据库中搜索对应课程的所有抽取所得实体。
- **方法**：`GET`
- **参数**： 无
- **返回**: 返回所查询课程的实体的知识点对象(知识点名称及描述其性质的字典).
- **请求示例**：`GET /course/entities/{title}`
- **响应示例**：
  ```json
  [
  {
    "name": "Stack"
  },
  {
    "name": "collections/collections.h"
  },
  {
    "message": "'error' was not declared in this scope"
  },
  {
    "name": "g++"
  },
  {
    "name": "CS1604Lib"
  },...
  ]
    ```   

## 4. 端点: `/course/rels/{title}`

- **描述**：在 Neo4j 数据库中搜索对应课程的所有抽取所得关系。
- **方法**：`GET`
- **参数**： 无
- **返回**: 返回所查询课程的知识点之间的关系.
- **请求示例**：`GET /course/rels/{title}`
- **响应示例**：
  ```json
  [
  {
    "start": {
      "name": "电荷密度"
    },
    "end": {
      "name": "左_右两电容并联"
    },
    "rel": [
      {
        "name": "电荷密度"
      },
      "RELATES_TO",
      {
        "name": "左_右两电容并联"
      }
    ]
  },
  {
    "start": {
      "name": "外界"
    },
    "end": {
      "name": "系统"
    },
    "rel": [
      {
        "name": "外界"
      },
      "ACTS_ON",
      {
        "name": "系统"
      }
    ]
  },
  {
    "start": {
      "name": "磁场"
    },
    "end": {
      "name": "磁感应强度B"
    },
    "rel": [
      {
        "name": "磁场"
      },
      "HAS_MAGNETIC_INDUCTION_STRENGTH",
      {
        "name": "磁感应强度B"
      }
    ]
  },...
  ]
    ```   

## 5. 端点：`/search/course/`

- **描述**：在 Neo4j 数据库中搜索包含用户指定字符串的节点属性。如果找到符合搜索条件的节点，则返回这些节点。如果没有找到结果，则返回一个错误信息，表明没有找到课程。
- **方法**：`GET`
- **参数**：
  - `q`（字符串）：用于搜索节点属性的查询字符串。
- **返回**：如果找到匹配的节点，则返回节点列表；如果没有找到，则返回空列表。
- **请求示例**：`GET /search/course?q=数学`
- **响应示例**：
  ```json
  [
  {
    "hours": 48,
    "code": "NIS231 2",
    "credits": 3,
    "name": "信息安全的数学基础（1）"
  },
  {
    "author": "牛顿",
    "title": "自然哲学的数学原理"
  }...
  ]
    ```

## 6. 端点：/search/course/rel

- **描述**：在 Neo4j 数据库中搜索包含用户指定字符串的关系属性。如果找到符合搜索条件的关系，则返回这些关系。如果没有找到结果，则返回一个错误信息，表明没有找到课程。
- **方法**：`GET`
- **参数**：
    - `q`（字符串）：用于搜索关系类型或属性的查询字符串。
- **返回**：返回匹配查询的关系数组。
- **请求示例**：`GET /search/course/rel?q=RELATED_TO`
- **响应示例**：

```json

[
  [
    {
      "name": "utiltimero"
    },
    "RELATED_TO",
    {
      "name": "utiltimercpp"
    }
  ],
  [
    {
      "name": "热力学过程的不可逆性"
    },
    "RELATED_TO",
    {
      "name": "可逆过程"
    }
  ],
  [
    {
      "name": "热力学过程的不可逆性"
    },
    "RELATED_TO",
    {
      "name": "不可逆过程"
    }
  ],...
]
```

## 7. 端点：/create/entities/{title}

- **描述**：根据输入参数在 Neo4j 数据库中创建具有指定属性和标签的新节点。该函数允许创建具有重复属性的节点。
- **方法**：`POST`
- **参数**：
        - `title`（字符串）：实体的标题。
        - `properties`（JSON 对象）：设置为新节点的属性和值的 JSON 对象。
- **返回**：返回数据库内部指示创建成功或失败的结果。
- **请求示例**：
```python
def test_create_node(self):
    params = {
        "name": "INTERRUPT",  # node的名字:只在创建过程中使用到,之后就无法获得了.
        "properties": {
            "context": "thread",
            "os": "linux",
        },  # node的属性,描述node的特征,可以用来进行匹配,查询等操作.
    }
    response = requests.post(
        f"{self.base_url}/create/entities/{self.example_course}", json=params
    )
```
- **响应示例**：HTTPStatus `200` code.

## 8. 端点：/update/entities/{title}

- **描述**：更新 Neo4j 数据库中通过其名称识别的特定节点的属性。修改节点以包括新的或更新的属性。
- **方法**：`POST`
- **参数**：
        - `title`（字符串）：要更新的节点的标题。
        - `new_properties`（JSON 对象）：更新的新属性和值的 JSON 对象。
- **返回**：返回数据库内部指示更新成功或失败的结果。
- **请求示例**：
```python
def test_update_node(self):
    params = {
        "name": "debugging",  # 用来匹配待更新节点的名字
        "new_properties": {
            "utils": "gdb"
        },  # 更新节点的新的属性,作为键值对的形式存在.
    }
    response = requests.post(
        f"{self.base_url}/update/entities/{self.example_course}", json=params
    )

```
- **响应示例**：HTTPStatus `200` code.

## 9. 端点：/delete/entities/{title}

- **描述**：根据其名称和类型在 Neo4j 数据库中删除一个节点。节点及其所有关系被删除。
- **方法**：POST
- **参数**：
        - `title`（字符串）：要删除的节点的标题。
- **返回**：返回数据库内部指示删除成功或失败的结果。
- **请求示例**：
```python
def test_delete_node(self):
    params = {"name": "debugging"}  # 用来匹配待删除节点的名字
    response = requests.post(
        f"{self.base_url}/delete/entities/{self.example_course}", json=params
    )
```
- **响应示例**：HTTPStatus `200` code.

## 10. 端点：/create/rel/{title}

- **描述**：在 Neo4j 数据库中创建两个指定节点之间的关系。关系通过其类型和属性来定义。
- **方法**：POST
- **参数**：
        - `name1`, `name2`（字符串）：起始和终点节点的名称。
        - `rel_type`（字符串）：关系的类型。
        - `properties`（JSON 对象）：关系的属性和值的 JSON 对象。
- **返回**：返回数据库内部指示创建成功或失败的结果。
- **请求示例**：
```python
def test_create_rel(self):
    params = {
        "name1": "StanfordCppLib",  # 用来匹配起始节点的名字
        "name2": "Queue",  # 用来匹配终点节点的名字
        "rel_type": "USES",  # 用来匹配连接起始节点和终点节点的关系的名字
        "properties": {
            "method": "exclusive"
        },  # 新创建关系的属性,作为键值对的形式存在.
    }
    response = requests.post(
        f"{self.base_url}/create/rel/{self.example_course}", json=params
    )

```
- **响应示例**：HTTPStatus `200` code.

## 11. 端点：/update/rel/{title}

- **描述**：更新 Neo4j 数据库中两个节点之间特定关系的属性。通过节点的名称和其类型识别关系。
- **方法**：POST
- **参数**：
        - `title`（字符串）：要更新的关系的标题。
        - `name1`, `name2`（字符串）：起始和终点节点的名称。
        - `rel_type`（字符串）：关系的类型。
        - `new_property`（JSON 对象）：更新的新属性和值的 JSON 对象。
- **返回**：返回数据库内部指示更新成功或失败的结果。
- **请求示例**：
```python
def test_update_rel(self):
    params = {
        "name1": "mingw32-make",  # 用来匹配起始节点的名字
        "name2": "Makefile linux",  # 用来匹配终点节点的名字
        "rel_type": "RELATED_TO",  # 用来匹配连接起始节点和终点节点的关系的名字
        "new_properties": {
            "method": "shared"
        },  # 更新关系的新的属性,作为键值对的形式存在.
    }
    response = requests.post(
        f"{self.base_url}/update/rel/{self.example_course}", json=params
    )
```
- **响应示例**：HTTPStatus `200` code.

## 12. 端点：/delete/rel/{title}

- **描述**：根据关系类型和涉及的节点名称在 Neo4j 数据库中删除两个节点之间的特定关系。
- **方法**：POST
- **参数**：
        - `title`（字符串）：要删除的关系的标题。
        - `rel_type`（字符串）：关系的类型。
        - `name1`, `name2`（字符串）：起始和终点节点的名称。
- **返回**：返回数据库内部指示删除成功或失败的结果。
- **请求示例**：
```python
def test_delete_rel(self):
    params = {
        "rel_type": "RELATED_TO",  # 用来匹配待删除关系的名字
        "name1": "mingw32-make",  # 用来匹配起始节点的名字
        "name2": "Makefile linux",  # 用来匹配终点节点的名字
    }
    response = requests.post(
        f"{self.base_url}/delete/rel/{self.example_course}", json=params
    )

```
- **响应示例**：HTTPStatus `200` code.

## 13. 端点：/vote/course/{title}

- **描述**：为通过其标题识别的特定课程增加投票计数器。此功能演示了数据库中管理计数器更新的简单方法。
- **方法**：`GET`
- **参数**：
        - `title`（字符串）：要投票的课程的标题。
- **返回**：计数器的当前值。
- **请求示例**：`GET /vote/course/{title}`
- **响应示例**：HTTPStatus `200` code.


注:
- /course/rels/CS1605 和 /course/rels/OS 返回的都是空列表,因为没有抽取到有效关系.
- /search/course?q=xx 和 /search/course/rel?q=xx 如果没找到的话,返回的都是空列表.
- 文档约定规范: 课程标题 __title__ 只能是以下其中一个: "__CS1604__", "__CS1605__", "__OS__", "__DAG__", "__UNIVERSITY_PHYSICS_1__", "__UNIVERSITY_PHYSICS_2__".
