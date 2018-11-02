FROM bartoszgorka/processing-massive-datasets:v1.0.0

# Add files with content
ADD unique_tracks.txt .
ADD triplets_sample_20p.txt .

# Convert files - set encoding
RUN iconv -sc -t UTF-8 -f ISO-8859-2 unique_tracks.txt > unique_tracks_serialized.txt

# Clear image
RUN rm unique_tracks.txt

# Install python3 extra deps
ADD requirements.txt .
RUN pip3 install -r requirements.txt

# Set dateID
RUN gawk -F'<SEP>' '{split(strftime("%Y %m", $3), arr, " "); print $0"<SEP>"((arr[1] - 2000) * 12 + arr[2]);}' triplets_sample_20p.txt > samples_formatted.txt
RUN rm triplets_sample_20p.txt

# Add exercise script
ADD mysql_exercise.py .

# Add start script
ADD run_db /sources/
RUN chmod +x /sources/run_db

# Set action on start container
ENTRYPOINT "/sources/run_db"
