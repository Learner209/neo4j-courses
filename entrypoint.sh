cd /home/courses/neo4j-instances/ports && ls | xargs -I{} /bin/bash -c 'cd {}; ./bin/neo4j start; cd ..;'

cd /app

exec python3 courses_async.py --database_dir "/home/courses/neo4j-instances/" --port 8000 --host "0.0.0.0"
