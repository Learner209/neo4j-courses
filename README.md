文档约定规范:
title: "CS1604", "CS1605", "OS", "DAG", "UNIVERSITY_PHYSICS_1", "UNIVERSITY_PHYSICS_2"

API 端点描述

/search/course:
    描述: 在 Neo4j 数据库中搜索包含用户指定字符串的节点的属性。如果找到符合搜索条件的节点则返回这些节点。如果没有找到结果，则返回一个错误，表明没有找到课程。

/search/course/rel:
    描述: 搜索数据库中的关系，这些关系的类型或属性包含指定的查询字符串。仅返回匹配查询的关系。

/create/entities/{title}:
    描述: 根据输入参数在 Neo4j 数据库中创建具有指定属性和标签的新节点。该函数允许创建具有重复属性的节点。

/update/entities/{title}:
    描述: 更新 Neo4j 数据库中通过其名称识别的特定节点的属性。修改节点以包括新的或更新的属性。

/delete/entities/{title}:
    描述: 根据其名称和类型在 Neo4j 数据库中删除一个节点。节点及其所有关系被删除。

/create/rel/{title}:
    描述: 在 Neo4j 数据库中创建两个指定节点之间的关系。关系通过其类型和属性来定义。

/update/rel/{title}:
    描述: 更新 Neo4j 数据库中两个节点之间特定关系的属性。通过节点的名称和其类型识别关系。

/delete/rel/{title}:
    描述: 根据关系类型和涉及的节点名称在 Neo4j 数据库中删除两个节点之间的特定关系。

/vote/course/{title}:
    描述: 为通过其标题识别的特定课程增加投票计数器。此功能演示了数据库中管理计数器更新的简单方法。


| 端点                     | 方法 | 描述                                     | 参数（关键）                                                      | 输出示例     | 输入示例                                                                                           |
|--------------------------|------|------------------------------------------|-------------------------------------------------------------------|--------------|----------------------------------------------------------------------------------------------------|
| /search/course           | GET  | 搜索包含查询字符串的节点的属性。         | q (查询字符串)                                                    | 节点列表     | https://localhost:{port}/search/course?q=physics                                                   |
| /search/course/rel       | GET  | 按类型或名称搜索包含查询字符串的关系。   | q (查询字符串)                                                    | 关系列表     | https://localhost:{port}/search/course/rel?q=physics                                               |
| /create/entities/{title} | GET  | 使用特定属性创建新节点。                 | title, alias, node_type, properties                               | 节点创建结果 | [create entities](tests/course_async_test.py#L9)                                                  |
| /update/entities/{title} | GET  | 更新通过唯一属性识别的节点的属性。       | title, identifying_property, new_properties, node_type            | 更新后的节点 | [update entities](tests/course_async_test.py#L20)                                                  |
| /delete/entities/{title} | GET  | 删除节点及其关系。                       | title, node_type, identifying_property                            | 删除结果     | [delete entities](tests/course_async_test.py#L31)                                                  |
| /create/rel/{title}      | GET  | 创建两个指定节点之间带有指定属性的关系。 | title, node_type1, node_type2, name1, name2, rel_type, properties | 关系创建结果 | [create rels](tests/course_async_test.py#L38)                                                      |
| /update/rel/{title}      | GET  | 更新两个节点之间关系的属性。             | title, name1, name2, rel_type, new_properties                     | 更新后的关系 | [update rels](tests/course_async_test.py#L52)                                                      |
| /delete/rel/{title}      | GET  | 删除两个节点之间的关系。                 | title, rel_type, name1, name2                                     | 删除结果     | [delete rels](tests/course_async_test.py#L64)                                                      |
| /vote/course/{title}     | GET  | 为课程增加投票计数器。                   | title                                                             | 投票增加结果 | https://localhsot:{port}/vote/course/CS1605                                                        |

