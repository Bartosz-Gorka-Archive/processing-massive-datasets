FROM python:3.7-stretch

LABEL maintainer="Bartosz Górka <bartosz.gorka@interia.eu>"

# Add files with content
ADD unique_tracks.txt .
ADD triplets_sample_20p.txt .

# Add exercise script
ADD exercise.py .

# Set action on start container
ENTRYPOINT python3 exercise.py
