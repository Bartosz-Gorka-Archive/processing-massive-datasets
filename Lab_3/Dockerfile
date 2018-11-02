FROM mariadb:latest

# Add files with datae
ADD unique_tracks.txt .
ADD triplets_sample_20p.txt .

# Convert files - set encoding
RUN iconv -sc -t UTF-8 -f ISO-8859-2 unique_tracks.txt > unique_tracks_serialized.txt

# Separate lines - when with | - insert it manually
RUN grep "|" unique_tracks_serialized.txt > with_separator.txt
RUN grep -v "|" unique_tracks_serialized.txt > without_separator.txt

# Replace <SEP> with | separator
RUN sed -i -e "s/<SEP>/\|/g" without_separator.txt

# Set python3
RUN apt-get -y update
RUN apt-get -y install python3 python3-pip gawk
RUN apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [ ! -e /usr/bin/python ]; then ln -sf /usr/bin/python3 /usr/bin/python; fi

# Add DateID column
RUN gawk -F'<SEP>' '{year = strftime("%Y", $3); month = strftime("%m", $3); print $1, $2, ((year - 2000) * 12 + month);}' triplets_sample_20p.txt > samples_formatted.txt

# Remove first column from file
RUN cut -d "|" -f2- without_separator.txt > unique_tracks_formatted.txt

# Clear image
RUN rm unique_tracks_serialized.txt without_separator.txt unique_tracks.txt triplets_sample_20p.txt
RUN ls -a | grep -e '\.!.*.txt' | xargs -0 -r rm

# Install python3 extra deps
ADD requirements.txt .
RUN pip3 install -r requirements.txt

# Add exercise script
ADD mysql_exercise.py .

ADD run_db /sources/
RUN chmod +x /sources/run_db
ENTRYPOINT "/sources/run_db"
