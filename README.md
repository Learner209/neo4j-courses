# 数据库大作业知识图谱建立

# 项目管理与开发
### 使用到的开源仓库:

1. https://github.com/neo4j-examples/movies-python-bolt: 使用flask/FastAPI和d3.js,neo4j搭建的电影数据库
2. https://github.com/niterain/neo4j-instance: 操纵neo4j数据库的实用工具库
3. https://github.com/neo4j/neo4j-python-driver: neo4j驱动程序
4. https://github.com/ggerganov/llama.cpp: LLM inference工具
5. https://github.com/tiangolo/fastapi: 一个现代、快速（高性能）的网络框架，用于基于标准 Python 类型提示使用 Python 构建应用程序接口。
6. https://github.com/fxsjy/jieba: 中文分词工具



### 项目架构:


知识图谱的构建围绕一个多维度、多层次的数据处理流水线展开，该流水线融合了文本的预处理、分词、语义分析、大型语言模型推理以及知识图谱的构建与维护等多个关键技术组件。在设计过程中，我们对每一个组件进行了精心挑选和优化配置，以保证整个文本处理流程的高效性和准确性。这不仅包括对中文文本进行深度的分词和语义解析，还涉及到使用先进的自然语言处理模型（如LLM）来推理和生成符合neo4j命令格式的图谱数据。

为了进一步提升系统处理复杂查询的能力，我们将整个流水线进行有效的分工和隔离，同时也考虑了数据的可扩展性和可维护性，采用模块化的设计理念，使得每个组件都可以在不影响其他部分的基础上进行独立的升级和优化。

通过这样的系统架构设计，我们不仅能够确保文本数据从输入到处理再到输出的每一个步骤都能够高效、准确地执行，还能够为用户提供一个强大而灵活的框架，支持他们对课程内容进行深入的查询和分析。

流程图:

![](https://notes.sjtu.edu.cn/uploads/upload_46782f8f2e069a127c4fc254b28249c0.png)


#### 数据处理流水线


##### 文本提取与分段:

1. 输入阶段：
整个处理流程的起点是从先前环节获得的文本文件中提取信息。这些文本文件主要以中文撰写，包含了诸多教学课程的详细描述以及相关教学资料。这些文件源自上游任务，其内容涵盖了从课程大纲,具体教学目标,课程公告,课程文档等多个维度，为后续的文本处理和知识图谱构建提供了丰富的数据基础。

2. 处理阶段：
在文本处理阶段，我们采用了jieba分词工具进行中文文本的分割。

3. 分类阶段：
经过精确的分词后，我们将文本中的词汇按照其所属的课程内容进行分类整理。例如，操作系统（OS）、大学物理一（University-physics）、计算机科学课程（CS1604, CS1605）等，每一类课程都根据其特定的教学内容和目标进行独立分类。这种分类不仅基于课程名称，还深入到课程内容的具体特点，如理论侧重、实践操作等，以确保后续生成的知识图谱在精确性和实用性上都能达到最优状态。通过这样的精细化管理，每个课程相关的文本数据都被有序地组织起来，便于进行更深层次的分析和应用。

此外，这一阶段的工作还包括对分词结果的进一步校验和优化，确保从源文本中提取的信息能够无缝对接到下一阶段的语言模型推理和知识图谱的构建过程中，从而形成一个从文本提取到知识应用的闭环处理流程。通过这种综合性的文本处理策略，我们能够更好地捕捉和表现教育内容的深层结构和内在联系.

##### LLM推理:

1. 处理器配置与调用：
在本项目中，LLM的推理是通过llama.cpp项目实现的。我们选择了 70b-llama3-chat gguf模型，这个LLM专为处理和生成复杂的文本数据而设计。通过该模型，我们能够处理大量的分词结果，并转化为具有实际应用价值的结构化数据。llama.cpp项目不仅提供了模型调用的接口，还优化了数据输入和输出流程，确保语言模型可以在高效和稳定的环境中运行。

2. 推理过程：
在推理过程中，通过jieba分词工具处理后的文本数据将作为输入，输入到LLM中。这些数据包含了从原始文本中提取的关键词汇和词组，每一项都蕴含着丰富的语义信息。70b-llama3-chat gguf模型将这些输入分析并理解其深层语义，然后生成符合Neo4j图数据库命令格式的输出。这意味着模型不仅仅是在进行文本生成，更是在进行逻辑推理和结构化转换，直接输出可以被图数据库理解和执行的命令。

3. 校正与后处理：
由于自动推理过程可能存在不可避免的误差，例如格式错误或语义不准确等问题，我们设计了一套手动过滤和post-processing工具来进行校正。这些工具包括自定义的脚本和程序，能够对LLM的输出结果进行细致的审查和修改。校正过程中，我们特别关注保持数据的一致性和准确性，确保每一条生成的Neo4j命令都严格符合图数据库的操作规范。此外，这一阶段的工作也涉及到与专业知识图谱构建者的协作，他们对模型的输出进行专业评估，以保证知识图谱的质量和实用性。


LLAMA3:使用的prompt:
```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>   
You are a helpful and smart neo4j developer and also a person with expertise in a wide range of domains who answers yser queries with accurate responses.
<|eot_id|><|start_header_id|>user<|end_header_id|>                         
For the following text, please extract the entities and relationships
(in elegant chinese) between these entities (if has one) and 
then return the extracted entities and relationships using neo4j command format. The text is : {text}  
Just return the required template, keep your answer as simple and concise as possible, leave out any explanations and descriptions. 
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
```
运行llama.cpp的参数和命令:
```shell
./main -ngl 32 -m ./pretrained_checkpoints/Meta-Llama-3-70B-Instruct-Q4_K_M.gguf --color -c 4096 --temp 0.7 --repeat_penalty 1.1. --n-predict -1 -p $prompt 
```


##### 知识图谱构建与存储

在从LLM模型中提取完成的实体与关系数据，我们将其按照课程分类进行有序存储。每个课程相关的数据被细致地保存在磁盘上的特定位置，以便于系统对这些数据进行高效的读取和检索。这种按课程细分的存储策略，不仅有助于维护数据的结构化和可查询性，也便于在未来进行数据的更新与维护工作。存储过程中，我们采用了先进的数据编码和压缩技术，确保数据在保存时占用最小的磁盘空间，同时保持快速的访问速度。

1. 多实例管理的复杂性及其解决方案：
由于Neo4j社区版的使用限制，我们面临着只能访问单一数据库的技术挑战。为了突破这一限制，我们采取了创新的多实例管理策略。首先，通过专门的工具从官方网站下载Neo4j的执行文件，然后对这些文件的配置进行精确修改，使得我们能够启动多个Neo4j实例，每个实例监听不同的端口。这种方法不仅有效地扩展了系统的数据处理能力，还增强了数据操作的灵活性和系统的可扩展性。

通过修改配置文件，我们能够详细设定每个实例的运行参数，如内存使用限制、并发连接数、以及数据同步策略等，确保每个实例都能在最优的条件下运行，从而提升整个系统的性能和稳定性。此外，这种多实例运行方式还允许我们针对不同的用户需求和数据安全需求，将特定课程或数据类型隔离在不同的数据库实例中，从而在提升服务质量的同时，增加数据安全性。

##### 知识图谱交互框架:

1. 技术选型与架构设计：
在构建知识图谱交互框架时，我们选择了FastAPI框架，这是一种现代、快速（高性能）的Web框架，用于构建API与Web应用程序。FastAPI支持异步编程模型，能够处理大量并发请求，这对于数据密集型的操作如知识图谱查询尤为重要。此外，该框架提供了自动交互文档，极大简化了前后端开发者的协作。后端通过高效的Neo4j驱动与数据库进行交互，这种驱动支持通过Cypher查询语言进行高效的图数据操作，确保了数据查询与更新的速度和准确性。

2. 功能实现的深度整合：
系统功能覆盖了增删查改（CRUD）操作，这是管理任何数据库系统中数据不可或缺的基本操作。通过FastAPI实现的接口，用户可以方便地执行对知识图谱中的实体和关系的查询、更新、添加和删除操作。特别地，系统还提供了查看特定课程的有向无环图（DAG）关系和实体的功能，这对于理解课程间的依赖和结构具有重要意义。例如，通过特定API端点，用户可以直接查询到课程的先修关系图，从而得到课程结构的直观表示。

3. API服务与端点设计：
我们设计了一系列的API端点，以支持各种数据操作和查询需求。例如，/dag/courses端点允许用户查询所有课程的先修关系图的实体，而/course/entities/{title}和/course/rels/{title}端点则提供了搜索指定课程的实体和关系的功能。这些API端点的设计考虑了易用性和功能性，确保用户能够快速而准确地获取所需数据。详细的API文档和示例使得开发者可以轻松理解和使用这些接口，促进了系统的开放性和可扩展性。


##### 详细的API说明:

文档约定规范: 
课程标题title只能是以下其中一个: "CS1604", "CS1605", "OS", "DAG", "UNIVERSITY_PHYSICS_1", "UNIVERSITY_PHYSICS_2".

1. /search/course:
    描述: 在 Neo4j 数据库中搜索包含用户指定字符串的节点的属性。如果找到符合搜索条件的节点则返回这些节点。如果没有找到结果，则返回一个错误，表明没有找到课程。

2. /search/course/rel:
    描述: 搜索数据库中的关系，这些关系的类型或属性包含指定的查询字符串。仅返回匹配查询的关系。

3. /create/entities/{title}:
    描述: 根据输入参数在 Neo4j 数据库中创建具有指定属性和标签的新节点。该函数允许创建具有重复属性的节点。

4. /update/entities/{title}:
    描述: 更新 Neo4j 数据库中通过其名称识别的特定节点的属性。修改节点以包括新的或更新的属性。

5. /delete/entities/{title}:
    描述: 根据其名称和类型在 Neo4j 数据库中删除一个节点。节点及其所有关系被删除。

6. /create/rel/{title}:
    描述: 在 Neo4j 数据库中创建两个指定节点之间的关系。关系通过其类型和属性来定义。

7. /update/rel/{title}:
    描述: 更新 Neo4j 数据库中两个节点之间特定关系的属性。通过节点的名称和其类型识别关系。

8. /delete/rel/{title}:
    描述: 根据关系类型和涉及的节点名称在 Neo4j 数据库中删除两个节点之间的特定关系。

9. /vote/course/{title}:
    描述: 为通过其标题识别的特定课程增加投票计数器。此功能演示了数据库中管理计数器更新的简单方法。


| 端点                     | 方法 | 描述                                     | 参数（关键）                                                      | 输出示例                                                           | 输入示例                                                |
|--------------------------|------|------------------------------------------|-------------------------------------------------------------------|--------------------------------------------------------------------|---------------------------------------------------------|
| /dag/courses             | GET  | 搜索课程先修关系图的所有实体.            | None                                                              | [{"hours":8,"name":"形势与政策",code:"MARX105","credits":0.5},...] | https://localhost:{port}/dag/courses                    |
| /dag/rels                | GET  | 搜索课程先修关系图的所有关系。           | None                                                              | [{"prerequisite":{...},"end":{...},"rel":{...}},...]               | https://localhost:{port}/dag/rels                       |
| /course/entities/{title} | GET  | 搜索指定课程的实体。                     | None                                                              | [{key1:value1},{key2:value2},{key3,value3},...]                    | https://localhost:{port}/course/entities/{title}        |
| /course/rels/{title}     | GET  | 搜索指定课程的关系。                     | None                                                              | [{"start":{...},"end":{...},"rel":{...}},...]                      | https://localhost:{port}/course/rels/{title}            |
| /search/course           | GET  | 搜索包含查询字符串的节点的属性。         | q (查询字符串)                                                    | [{key1:value1},{key2:value2},{key3:value3},...]                    | https://localhost:{port}/search/course?q=physics        |
| /search/course/rel       | GET  | 按类型或名称搜索包含查询字符串的关系。   | q (查询字符串)                                                    | [[start_node,rel_name,dst_node],...]                               | https://localhost:{port}/search/course/rel?q=RELATED_TO |
| /create/entities/{title} | GET  | 使用特定属性创建新节点。                 | title, alias, node_type, properties                               | 数据库内部的返回结果                                               | [create entities](tests/course_async_test.py#L9)        |
| /update/entities/{title} | GET  | 更新通过唯一属性识别的节点的属性。       | title, identifying_property, new_properties, node_type            | 数据库内部的返回结果                                               | [update entities](tests/course_async_test.py#L22)       |
| /delete/entities/{title} | GET  | 删除节点及其关系。                       | title, node_type, identifying_property                            | 数据库内部的返回结果                                               | [delete entities](tests/course_async_test.py#L34)       |
| /create/rel/{title}      | GET  | 创建两个指定节点之间带有指定属性的关系。 | title, node_type1, node_type2, name1, name2, rel_type, properties | 数据库内部的返回结果                                               | [create rels](tests/course_async_test.py#L41)           |
| /update/rel/{title}      | GET  | 更新两个节点之间关系的属性。             | title, name1, name2, rel_type, new_properties                     | 数据库内部的返回结果                                               | [update rels](tests/course_async_test.py#L55)           |
| /delete/rel/{title}      | GET  | 删除两个节点之间的关系。                 | title, rel_type, name1, name2                                     | 数据库内部的返回结果                                               | [delete rels](tests/course_async_test.py#L69)           |
| /vote/course/{title}     | GET  | 为课程增加投票计数器。                   | title                                                             | 数据库内部的返回结果                                               | https://localhsot:{port}/vote/course/CS1605             |

注:
- /course/rels/CS1605 和 /course/rels/OS 返回的都是空列表,因为没有抽取到有效关系.
- /search/course?q=xx 和 /search/course/rel?q=xx 如果没找到的话,返回的都是空列表.



### 课程关系图谱展示

示例sql代码:
```sql

CREATE  (marx1_205:Course {code: 'MARX1 205', name: '形势与政策', credits: 0.5, hours: 8})
CREATE  (mil120_1:Course {code: 'MIL120 1', name: '军事理论', credits: 2.0, hours: 32})
CREATE  (cs1602:Course {code: 'CS1602', name: '计算导论', credits: 4.0, hours: 64})
CREATE  (cs1604:Course {code: 'CS1604', name: '程序设计原理与方法', credits: 4.0, hours: 64})
CREATE  (ee0501_h:Course {code: 'EE0501 H', name: '电路理论（荣誉）', credits: 3.0, hours: 48})
CREATE  (est250_1:Course {code: 'EST250 1', name: '数字电子技术', credits: 2.0, hours: 32})
CREATE  (phy125_1h:Course {code: 'PHY125 1H', name: '大学物理（荣誉）（1）', credits: 5.0, hours: 80})
CREATE  (phy125_2h:Course {code: 'PHY125 2H', name: '大学物理（荣誉）（2）', credits: 5.0, hours: 80})
CREATE  (phy125_3h:Course {code: 'PHY125 3H', name: '大学物理（荣誉）（3）', credits: 2.0, hours: 32})
CREATE  (math1_207:Course {code: 'MATH1 207', name: '概率统计', credits: 3.0, hours: 48})
CREATE  (ice3301:Course {code: 'ICE3301', name: '数字信号处理', credits: 3.0, hours: 48})
CREATE  (ai3603:Course {code: 'AI3603', name: '人工智能理论及应用', credits: 3.0, hours: 48})
CREATE  (cs3612:Course {code: 'CS3612', name: '机器学习', credits: 3.0, hours: 48})
CREATE  (ice260_5:Course {code: 'ICE260 5', name: '信号与系统（含复变函数）', credits: 4.0, hours: 64})
CREATE  (cs3324:Course {code: 'CS3324', name: '数字图像处理', credits: 3.0, hours: 48})
CREATE  (ice260_3:Course {code: 'ICE260 3', name: '计算机组成', credits: 4.0, hours: 64})
CREATE  (cs3601:Course {code: 'CS3601', name: '操作系统', credits: 3.0, hours: 48})
CREATE  (cs3604:Course {code: 'CS3604', name: '软件工程与项目管理', credits: 3.0, hours: 48})
CREATE  (cs4302:Course {code: 'CS4302', name: '并行与分布式程序设计', credits: 3.0, hours: 48})
CREATE  (est330_6:Course {code: 'EST330 6', name: '通信原理', credits: 5.0, hours: 80})
CREATE  (ice330_7:Course {code: 'ICE330 7', name: '无线通信原理与移动网络', credits: 3.0, hours: 48})
CREATE  (au2651:Course {code: 'AU2651', name: '控制理论', credits: 3.0, hours: 48})
CREATE  (au3307:Course {code: 'AU3307', name: '机器人学', credits: 2.0, hours: 32})
CREATE  (nis133_5:Course {code: 'NIS133 5', name: '网络信息安全概论', credits: 2.0, hours: 32})
CREATE  (nis331_6:Course {code: 'NIS331 6', name: '信息安全综合实践', credits: 3.0, hours: 48})
CREATE  (nis360_5:Course {code: 'NIS360 5', name: '密码工程实践', credits: 2.0, hours: 32})
CREATE  (ice331_1:Course {code: 'ICE331 1', name: '智能物联网', credits: 3.0, hours: 48})
CREATE  (au4606:Course {code: 'AU4606', name: '网络优化', credits: 3.0, hours: 48})
CREATE  (nis360_6:Course {code: 'NIS360 6', name: '云计算安全', credits: 2.0, hours: 32})
CREATE  (est250_2:Course {code: 'EST250 2', name: '模拟电子技术', credits: 2.0, hours: 32})
CREATE  (ice332_1:Course {code: 'ICE332 1', name: '视频编码与通信', credits: 3.0, hours: 48})
CREATE  (ice331_0:Course {code: 'ICE331 0', name: '光纤通信概论', credits: 2.0, hours: 32})
CREATE  (nis231_2:Course {code: 'NIS231 2', name: '信息安全的数学基础（1）', credits: 3.0, hours: 48})
CREATE  (nis433_3:Course {code: 'NIS433 3', name: '现代密码学', credits: 2.0, hours: 34})
CREATE  (marx1_205)-[:PREREQUISITE_FOR]->(mil120_1)
CREATE  (mil120_1)-[:PREREQUISITE_FOR]->(cs1602)
CREATE  (cs1602)-[:PREREQUISITE_FOR]->(cs1604)
CREATE  (ee0501_h)-[:PREREQUISITE_FOR]->(est250_1)
CREATE  (phy125_1h)-[:PREREQUISITE_FOR]->(phy125_2h)
CREATE  (phy125_2h)-[:PREREQUISITE_FOR]->(phy125_3h)
CREATE  (est250_1)-[:PREREQUISITE_FOR]->(est250_2)
CREATE  (math1_207)-[:PREREQUISITE_FOR]->(ice3301)
CREATE  (ai3603)-[:PREREQUISITE_FOR]->(cs3612)
CREATE  (ice260_5)-[:PREREQUISITE_FOR]->(cs3324)
CREATE  (ice260_3)-[:PREREQUISITE_FOR]->(cs3601)
CREATE  (cs3604)-[:PREREQUISITE_FOR]->(cs4302)
CREATE  (est330_6)-[:PREREQUISITE_FOR]->(ice330_7)
CREATE  (au2651)-[:PREREQUISITE_FOR]->(au3307)
CREATE  (nis133_5)-[:PREREQUISITE_FOR]->(nis331_6)
CREATE  (nis360_5)-[:PREREQUISITE_FOR]->(ice331_1)
CREATE  (nis360_6)-[:PREREQUISITE_FOR]->(au4606)
CREATE  (ice260_5)-[:PREREQUISITE_FOR]->(ice332_1)
CREATE  (est250_2)-[:PREREQUISITE_FOR]->(ice3301)
CREATE  (est330_6)-[:PREREQUISITE_FOR]->(ice331_0)
CREATE  (nis231_2)-[:PREREQUISITE_FOR]->(nis433_3)
CREATE  (cs3612)-[:RECOMMENDED_BEFORE]->(ai3603)
CREATE  (cs1604)-[:IS_UPDATE_OF]->(cs1602)
CREATE  (cs3612)-[:IS_PREREQUISITE_FOR_ADVANCED_COURSE]->(cs4302)
CREATE  (ai3603)-[:IS_CO_REQUISITE]->(cs3612)

```
在neo4j面板上展示的可视化结果:

![](https://notes.sjtu.edu.cn/uploads/upload_a8f6af64ffba33e9a2369659ecee54ac.png)

### 知识点结构图谱
- 对于每个课程，展示课程内各个知识点之间的层级和关联关系。

#### 课程CS1604示例代码:


```sql
CREATE (实验:Experiment {name:"Assignment 1"})
CREATE (题目:Question {name:"C++基础语法"})
CREATE (知识点:KnowledgePoint {name:"C++基本表达式"})
CREATE (编程风格:CodingStyle {name:"Code Style Guide"})
CREATE (环境变量:EnvironmentVariable {name:"Path"})
CREATE (gplusplus:Compiler {name:"g++"})
CREATE (judgerexe:Judger {name:"judger.exe"})
CREATE (stanfordcpplib:Library {name:"StanfordCppLib"})
CREATE (adt:AbstractDataType {name:"ADT"})
CREATE (collectionclasses:CollectionClasses {name:"Collection Classes"})
CREATE (vector:Vector {name:"Vector"})
CREATE (map:Map {name:"Map"})
CREATE (set:Set {name:"Set"})
CREATE (queue:Queue {name:"Queue"})
CREATE (stack:Stack {name:"Stack"})
CREATE (实验)-[:包含]->(题目)
CREATE (题目)-[:对应]->(知识点)
CREATE (编程风格)-[:规范]->(环境变量)
CREATE (gplusplus)-[:配置]->(环境变量)
CREATE (judgerexe)-[:使用]->(gplusplus)
CREATE (stanfordcpplib)-[:提供]->(adt)
CREATE (collectionclasses)-[:属于]->(stanfordcpplib)
CREATE (vector)-[:是]->(collectionclasses)
CREATE (map)-[:是]->(collectionclasses)
CREATE (set)-[:是]->(collectionclasses)
CREATE (queue)-[:是]->(collectionclasses)
CREATE (stack)-[:是]->(collectionclasses)
CREATE (f:File {name:"collections/collections.h"})
CREATE (e:Error {message:"'error' was not declared in this scope"})
CREATE (c:Compiler {name:"g++"})
CREATE (l:Library {name:"CS1604Lib"})
CREATE (p:Program {name:"CS1604Lib"})

```
##### 可视化结果:
![](https://notes.sjtu.edu.cn/uploads/upload_af3c5847402557af2818c3aff20c8d6a.png)


#### 大学物理课程1示例代码展示:

##### 
```sql

CREATE (非理想气体 {name:"非理想气体"})
CREATE (单原子气体 {name:"单原子气体"})
CREATE (双原子气体 {name:"双原子气体"})
CREATE (多原子气体 {name:"多原子气体"})
CREATE (热容比 {name:"热容比"})
CREATE (摩尔热容 {name:"摩尔热容"})
CREATE (定压摩尔热容 {name:"定压摩尔热容"})
CREATE (橡皮带 {name:"橡皮带"})
CREATE (Ideal_Gas:Entity {name:"理想气体"})
CREATE (Carnot_Cycle:Entity {name:"卡诺循环"})
CREATE (Thermodynamic_System:Entity {name:"热力学系统"})
CREATE (Heat_Source:Entity {name:"热源"})
CREATE (Low_Temperature_Heat_Source:Entity {name:"低温热源"})
CREATE (High_Temperature_Heat_Source:Entity {name:"高温热源"})
CREATE (Refrigerator:Entity {name:"冰箱"})
CREATE (Air_Conditioner:Entity {name:"空调"})
CREATE (Heat_Pump:Entity {name:"热泵"})
CREATE (Otto_Cycle:Entity {name:"奥托循环"})
CREATE (Molecular_Ideal_Gas:Entity {name:"双原子分子理想气体"})
CREATE (工质:Entity {name:"Working Substance"})
CREATE (窗中:Entity {name:"Window"})
CREATE (贫噜:Entity {name:"Poor Lu"})
CREATE (核电厂)-[:产出 {relationship:"produces"}]->(核反应热功率)
CREATE (理想专体温标)-[:等价 {relationship:"equivalent"}]->(热力学温标)
CREATE (卡诺定理)-[:描述 {relationship:"describes"}]->(可逆卡诺循环)
CREATE (克劳修斯不等式)-[:等价 {relationship:"equivalent"}]->(可逆卡诺循环)
CREATE (熵)-[:是 {relationship:"is"}]->(热力学系统)
CREATE (冰)-[:在 {relationship:"in"}]->(恒温热库)
CREATE (一定质量化学纯的气体)-[:经历 {relationship:"experiences"}]->(可逆绝热过程)
CREATE (绝热系统)-[:是 {relationship:"is"}]->(孤立系统)
CREATE (非平衡态)-[:转化 {relationship:"transforms"}]->(平衡态)
CREATE (玻耳兹曼关系)-[:等价 {relationship:"equivalent"}]->(玻耳兹曼引入了熵的统计表述)
CREATE (热力学概率)-[:描述 {relationship:"describes"}]->(粒子系统)
CREATE (宏观态)-[:组成 {relationship:"comprises"}]->(微观态)
CREATE (个粒子分布)-[:等于 {relationship:"equals"}]->(左右状态数)
CREATE (玻耳兹曼墓碑)-[:记录 {relationship:"records"}]->(玻耳兹曼关系)
CREATE (光脉冲)-[:反射 {relationship:"reflects"}]->(镜上反射)
CREATE (玻璃板)-[:具有 {relationship:"has"}]->(折射率)
CREATE (:Entity {name: "光速"})
CREATE (:Concept {name: "相对论"})
CREATE (:Concept {name: "力学公式"})
CREATE (:Concept {name: "能量守恒定律"})
CREATE (:Concept {name: "质量守恒定律"})
CREATE (:Concept {name: "质能守恒定律"})
CREATE (:Entity {name: "物体"})-[:HAS {type: "质量"}]->(:Entity {name: "质量"})
CREATE (:Entity {name: "质量"})-[:EQUALS {type: "相对论质量"}]->(:Entity {name: "相对论质量"})
CREATE (:Entity {name: "动能"})-[:IS_A {type: "能量的一种形式"}]->(:Concept {name: "能量"})
CREATE (:Entity {name: "静能"})-[:IS_A {type: "能量的一种形式"}]->(:Concept {name: "能量"})
CREATE (:Entity {name: "总能"})-[:EQUALS {type: "动能 + 静能"}]->(:Entity {name: "动能"}), (:Entity {name: "静能"})
CREATE (:Entity {name: "相对论质量"})-[:IS_A {type: "能量的量度"}]->(:Concept {name: "能量"})
CREATE (:Entity {name: "力学"})-[:STUDIES {type: "物体运动"}]->(:Entity {name: "物体"})
CREATE (:Entity {name: "片"})-[:PART_OF {type: "系统的一部分"}]->(:Entity {name: "系统"})
CREATE (:Entity {name: "核"})-[:CENTER_OF {type: "原子的中心"}]->(:Entity {name: "原子"})
CREATE (:Entity {name: "电子"})-[:ORBITS_AROUND {type: "核"}]->(:Entity {name: "核"})
CREATE (:Entity {name: "质点"})-[:IS_A {type: "片的一种形式"}]->(:Entity {name: "片"})
CREATE (:Entity {name: "光速"})-[:IS {type: "自然界的极限速度"}]->(:Concept {name: "自然界"})

```

## 知识图谱在我们的应用中发挥的作用:

### 课程先修关系DAG图:
- 展示课程之间的先修后续关系。(DAG)
- 通过箭头和线条表示课程之间的依赖性，帮助学生规划学习路径。
- 通过树状图或思维导图的形式，帮助学生理解课程内容的组织结构。

### 跨课程知识点关联图谱:
- 展示不同课程中相互关联的知识点。
- 通过网络图的形式，揭示不同课程间的交叉和互补，促进跨学科学习。

### 学习进度跟踪图谱:
- 根据学生的学习行为和完成情况，动态生成个人学习路径图。
- 通过进度条或时间线的形式，展示学生的学习进度和成就。

## 留给前端的说明(TODO):
### 交互式课程地图
- 允许学生通过点击和拖动来探索课程之间的关系。
- 提供放大、缩小和搜索功能，以便快速定位感兴趣的课程或知识点。

### 知识点探索器
- 学生可以通过选择一个知识点，系统展示与之相关联的其他知识点和课程。
- 通过弹出窗口或侧边栏展示详细信息，如概念解释、相关作业和讨论话题。

### 可视化数据分析
- 利用知识图谱分析学习数据，如学生成绩分布、课程难度等。
- 通过图表和仪表板的形式，为教师提供课程管理和改进的依据。

## 知识图谱的未来展望

### 资源推荐图谱
- 根据学生的学习历史和偏好，通过NLP等相关技术,推荐相关的课件、作业、参考资料等。
- 通过雷达图或热力图的形式，展示资源的推荐度和相关性。

### 学习路径规划器
- 学生输入自己的学习目标和兴趣，系统生成个性化的学习路径。
- 结合知识图谱和算法推荐，提供最优的学习顺序和资源。

### 协作学习网络
- 展示学生之间的学习互动和讨论，如论坛帖子、小组作业等。
- 通过社区图谱的形式，促进学生之间的交流和合作。
