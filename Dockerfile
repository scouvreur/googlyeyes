FROM continuumio/miniconda3

WORKDIR /app

# Create the environment
COPY setup.py .
COPY README.md .
COPY googlyeyes/ googlyeyes/
COPY resources/ resources/

# Install dependencies
RUN conda update -n base -c defaults conda
RUN conda install -c conda-forge requests Flask Flask-RESTful imutils dlib opencv numpy
RUN pip install -e .

# Run when container is started
ENTRYPOINT ["python", "googlyeyes/server.py"]
EXPOSE 5000
