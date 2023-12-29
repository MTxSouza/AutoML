# downloading base image
FROM mongo:latest

# running container
RUN ["docker", "run", "-d", "--rm" \
    "--name", "automl-db", \
    "-p", "80:27017", \
    "-e", "MONGO_INITDB_ROOT_USERNAME=admin", \
    "-e", "MONGO_INITDB_ROOT_PASSWORD=1234", \
    "mongo:latest"]
