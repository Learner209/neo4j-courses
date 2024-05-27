#!/usr/bin/env python
import argparse
import logging
import os
from contextlib import asynccontextmanager
from typing import Optional, cast

import neo4j
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from neo4j import AsyncGraphDatabase
import yaml

PATH = os.path.dirname(os.path.abspath(__file__))
SHARED_CONTEXT = {}
COURSES = [
    "CS1604",
    "CS1605",
    "OS",
    "DAG",
    "UNIVERSITY_PHYSICS_1",
    "UNIVERSITY_PHYSICS_2",
]
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


@asynccontextmanager
async def lifespan(app: FastAPI, filepath: str):
    with open(filepath, "r") as file:
        # Load the YAML file
        config = yaml.safe_load(file)
    SHARED_CONTEXT["driver"] = {}
    SHARED_CONTEXT["config"] = {}
    SHARED_CONTEXT["vote"] = {}
    for course in COURSES:
        port = config["databases"][course]["port"]
        database_path = os.path.join(args.database_dir, "ports", port)
        db_config = {
            "db-name": open(os.path.join(database_path, "db-name")).read().strip(),
            "bolt-port": open(os.path.join(database_path, "bolt-port")).read().strip(),
            "shell-port": open(os.path.join(database_path, "shell-port"))
            .read()
            .strip(),
            "neo4j_executable_path": os.path.join(database_path, "bin", "neo4j"),
            "cypher_shell_executable_path": os.path.join(
                database_path, "bin", "cypher-shell"
            ),
            "username": config["databases"][course]["username"],
            "password": config["databases"][course]["password"],
        }
        db_config["url"] = f"neo4j://localhost:{db_config['bolt-port']}"

        SHARED_CONTEXT["driver"][course] = AsyncGraphDatabase.driver(
            db_config["url"], auth=(db_config["username"], db_config["password"])
        )
        SHARED_CONTEXT["config"][course] = db_config
        SHARED_CONTEXT["vote"][course] = 0
    yield
    for driver in SHARED_CONTEXT["driver"].values():
        await driver.close()


def get_driver(course) -> neo4j.AsyncDriver:
    return SHARED_CONTEXT["driver"][course]


from fastapi.middleware.cors import CORSMiddleware

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8080)
parser.add_argument("--host", type=str, default="127.0.0.1")
parser.add_argument("--config_path", type=str, default="./config.yaml")
parser.add_argument("--database_dir", type=str, default="~/neo4j-instances")
args = parser.parse_args()

app = FastAPI(lifespan=lambda app: lifespan(app, args.config_path))
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_index():
    return FileResponse(os.path.join(PATH, "static", "index.html"))


@app.get("/dag/courses")
async def get_dag_courses(limit: int = 100):
    records = await get_driver("DAG").execute_query(
        """
            MATCH (n)
            RETURN *
        """,
        database_=DATABASE,
        routing_="r",
        limit=limit,
        result_transformer_=neo4j.AsyncResult.data,
    )
    records = [record for record in records if record["n"]]
    extract_course_fn = lambda record: {
        "hours": record["n"]["hours"],
        "name": record["n"]["name"],
        "code": record["n"]["code"],
        "credits": record["n"]["credits"],
    }
    courses = [extract_course_fn(record) for record in records]
    print(courses)
    return courses


@app.get("/dag/rels")
async def get_dag_rels(limit: int = 100, return_graph: bool = True):
    records = await get_driver("DAG").execute_query(
        """
            MATCH (n)-[r]->(m)
            RETURN *
        """,
        database_=DATABASE,
        routing_="r",
        limit=limit,
        result_transformer_=neo4j.AsyncResult.data,
    )
    extract_rel_fn = lambda record: {
        "prerequisite": record["n"],
        "end": record["m"],
        "rel": record["r"],
    }
    rels = [extract_rel_fn(record) for record in records]
    print(rels)
    if return_graph:
        nodes = []
        links = []
        for rel in rels:
            nodes.append(rel["prerequisite"])
            nodes.append(rel["end"])
            links.append(
                {
                    "source": nodes.index(rel["prerequisite"]),
                    "target": nodes.index(rel["end"]),
                }
            )
        return {"nodes": nodes, "links": links}

    return rels


@app.get("/course/entities/{title}")
async def get_course_entities(title: str):
    results = await get_driver(title).execute_query(
        """
            MATCH (n)
            RETURN *
        """,
        title=title,
        database_=DATABASE,
        routing_="r",
        result_transformer_=neo4j.AsyncResult.data,
    )
    if results is None:
        raise HTTPException(status_code=404, detail="Course not found")
    entities = [result["n"] for result in results if result["n"]]
    print(entities)

    return entities


@app.get("/course/rels/{title}")
async def get_course_rels(title: str, return_graph: bool = False):
    results = await get_driver(title).execute_query(
        """
            MATCH (n)-[r]->(m)
            RETURN *
        """,
        title=title,
        database_=DATABASE,
        routing_="r",
        result_transformer_=neo4j.AsyncResult.data,
    )
    if results is None:
        raise HTTPException(status_code=404, detail="Course not found")

    extract_rel_fn = lambda record: {
        "start": record["n"],
        "end": record["m"],
        "rel": record["r"],
    }
    rels = [extract_rel_fn(record) for record in results]
    print(rels)
    if return_graph:
        nodes = []
        links = []
        for rel in rels:
            nodes.append(rel["start"])
            nodes.append(rel["end"])
            links.append(
                {
                    "source": nodes.index(rel["start"]),
                    "target": nodes.index(rel["end"]),
                }
            )
        return {"nodes": nodes, "links": links}

    return rels


@app.get("/search/course")
async def get_course_search(q: Optional[str] = None):
    ans = []
    for course in COURSES:
        results = await get_driver(course).execute_query(
            f"""
                MATCH (n)
                WHERE any(key in keys(n) WHERE n[key] CONTAINS '{q}')
                RETURN n
                """,
            title=q,
            database_=DATABASE,
            routing_="r",
            result_transformer_=neo4j.AsyncResult.data,
        )
        ans.extend(results)
    if not ans:
        raise HTTPException(status_code=404, detail="Course not found")
    print(ans)
    ans = [single_ans["n"] for single_ans in ans if single_ans["n"]]

    return ans


@app.get("/search/course/rel")
async def get_course_rel_search(q: Optional[str] = None):
    if q is None:
        raise HTTPException(status_code=400, detail="Query parameter is required")

    ans = []
    for course in COURSES:
        results = await get_driver(course).execute_query(
            f"""
            MATCH (a)-[r]->(b) WHERE toString(TYPE(r)) CONTAINS "{q}" or r.name CONTAINS "{q}" return a,b,r;
            """,
            title=q,
            database_=DATABASE,
            routing_="r",
            result_transformer_=neo4j.AsyncResult.data,
        )
        results = [result for result in results if result["a"] and result["b"]]
        ans.extend(results)

    print(ans)
    if not ans:
        raise HTTPException(status_code=404, detail="Course not found")

    # Assume we want to return only the 'r' part of each result
    return [single_ans["r"] for single_ans in ans]


@app.get("/create/entities/{title}")
async def create_node(title: str):
    if title not in COURSES:
        raise HTTPException(status_code=404, detail="Course not found")
    alias = "os_concepts"
    node_type = "INTERRUPT"
    properties = {"context": "thread", "os": "linux"}
    query = f"CREATE ({alias}:{node_type} $properties) " f"RETURN {alias}"
    results = await get_driver(title).execute_query(query_=query, properties=properties)
    # Note: node with the exactly the same params is allowed to be created multiple times
    return results


@app.get("/update/entities/{title}")
async def update_node(title: str):
    if title not in COURSES:
        raise HTTPException(status_code=404, detail="Course not found")
    identifying_property = "debugging"
    new_properties = {"utils": "gdb"}
    node_type = "Entity"
    query = (
        f"MATCH (n:{node_type}) "
        "WHERE n.name = $name "
        "SET n += $new_properties "
        "RETURN n"
    )
    print(query)
    results = await get_driver(title).execute_query(
        query_=query, name=identifying_property, new_properties=new_properties
    )
    print(results)


@app.get("/delete/entities/{title}")
async def delete_node(title: str):
    node_type = "Entity"
    identifying_property = "debugging"
    query = f"MATCH (n:{node_type}) " "WHERE n.name = $name " "DETACH DELETE n"
    print(query)
    results = await get_driver(title).execute_query(
        query_=query, name=identifying_property
    )

    print(results)


@app.get("/create/rel/{title}")
async def create_rel(title: str):
    if title not in COURSES:
        raise HTTPException(status_code=404, detail="Course not found")

    # Define nodes and rel properties
    node_type1 = "Entity"
    node_type2 = "Entity"
    name1 = "StanfordCppLib"
    name2 = "Queue"
    rel_type = "USES"
    properties = {"method": "exclusive"}

    # Cypher query to create a rel
    query = (
        f"MATCH (a:{node_type1}), (b:{node_type2}) "
        f"WHERE a.name = $name1 AND b.name = $name2 "
        f"CREATE (a)-[r:{rel_type} $properties]->(b) "
        f"RETURN a, r, b"
    )
    results = await get_driver(title).execute_query(
        query_=query, name1=name1, name2=name2, properties=properties
    )
    return results


@app.get("/update/rel/{title}")
async def update_rel(title: str):
    if title not in COURSES:
        raise HTTPException(status_code=404, detail="Course not found")

    name1 = "mingw32-make"
    name2 = "Makefile linux"
    rel_type = "RELATED_To"
    new_properties = {"method": "shared"}

    # Cypher query to update a rel
    query = (
        f"MATCH (a)-[r:{rel_type}]->(b) "
        f"WHERE a.name = $name1 AND b.name = $name2 "
        f"SET r += $new_properties "
        f"RETURN a, r, b"
    )
    results = await get_driver(title).execute_query(
        query_=query, name1=name1, name2=name2, new_properties=new_properties
    )
    return results


@app.get("/delete/rel/{title}")
async def delete_rel(title: str):
    if title not in COURSES:
        raise HTTPException(status_code=404, detail="Course not found")

    rel_type = "RELATED_TO"
    name1 = "mingw32-make"
    name2 = "Makefile linux"

    # Cypher query to delete a rel
    query = (
        f"MATCH (a)-[r:{rel_type}]->(b) "
        f"WHERE a.name = $name1 AND b.name = $name2 "
        f"DELETE r"
    )
    results = await get_driver(title).execute_query(
        query_=query, name1=name1, name2=name2
    )
    return results


@app.get("/vote/course/{title}")
async def vote_course(title: str):
    if title not in COURSES:
        raise HTTPException(status_code=404, detail="Course not found")
    SHARED_CONTEXT["vote"][title] += 1
    return 1


if __name__ == "__main__":
    import uvicorn
    import argparse

    logging.root.setLevel(logging.INFO)
    logging.info("Starting on port: %d, host: %s", args.port, args.host)

    uvicorn.run(app, port=args.port, host=args.host)
