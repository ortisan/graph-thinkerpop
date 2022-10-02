# Graphs Demo with Tinkerpop

## Start

```sh
# Starting gremlin-server(8182) and gremlin-visualizer(3000)
docker-compose up --build
# Configuring project
poetry init
# Run formatter and lint
poetry run autoflake --expand-star-imports --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --recursive --in-place . && poetry run isort . && poetry run black .
# Creating graph
python main.py
```

## Gremlin Console 
Configuring gremlin-console to reach docker container of gremlin-server:

- Clone tinkerpop/gremlin-console and create custom remote file point to docker dns internal:

    ```sh
    echo "hosts: [host.docker.internal]
    port: 8182
    serializer: { className: org.apache.tinkerpop.gremlin.driver.ser.GraphBinaryMessageSerializerV1, config: { serializeResultToString: true }}" > conf/remote-docker.yaml
    ```
- Rebuild the tinkerpop/gremlin-console:
    ```sh
    mvn clean install
    docker build --build-arg GREMLIN_CONSOLE_DIR=. -t tentativafc/gremlin-console .
    docker push tentativafc/gremlin-console
    ```
- Start gremlin-console:
    ```sh
    docker run-ti tentativafc/gremlin-console
    # Connects to remote server
    :remote connect tinkerpop.server conf/remote-docker.yaml
    :remote console
    ```
## Queries:
```sh
g.V().has("states","type","state").out().count()
g.V().has("states","type","state").sum()
g.V().has("states","type","state").values("received_date")
g.V().has("type","state").as('a').
      out().as('b').
      select('a','b').
        by(values("id_payment", 'received_date').fold())

g.V().has("type","state").as('a').out().as('b').math('b - a').by('received_date').index().
      unfold()

g.V().has("type","state").
  bothE().
  where(__.otherV().has("type","state"))
```
