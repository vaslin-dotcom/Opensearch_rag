# OpenSearch RAG POC — Full Reference

## 1. Docker — start OpenSearch (first time ever)
docker pull opensearchproject/opensearch:latest

docker run -d -p 9200:9200 -p 9600:9600 \
  -e "discovery.type=single-node" \
  -e "DISABLE_SECURITY_PLUGIN=true" \
  -v opensearch-data:/usr/share/opensearch/data \
  --name opensearch_node \
  opensearchproject/opensearch:latest

## 2. Docker — every time you reopen Codespace
sudo service docker start
docker start opensearch_node
curl -X GET "http://localhost:9200"

## 3. Docker — if container is broken/corrupted
docker rm -f opensearch_node
# then rerun the docker run command from section 1

## 4. Docker — useful checks
docker ps                     # running containers
docker ps -a                  # all containers (incl. stopped)
docker logs opensearch_node   # debug crashes

