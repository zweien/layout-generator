docker rmi -f layout-generator:latest
docker build -t layout-generator:latest .
docker run --rm -v $(pwd):/home/fenics/layout layout-generator:latest pip install -U .[dev]
pytest