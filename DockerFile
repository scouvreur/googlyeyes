FROM ubuntu
FROM continuumio/miniconda3

WORKDIR /app

# Create the environment
COPY environment.yml .
COPY pytest.ini .
COPY setup.py .
COPY README.md .
COPY googlyeyes/ googlyeyes/
COPY resources/ resources/
COPY tests/ tests/
RUN ls -la .

# Install dependencies
RUN conda update -n base -c defaults conda
RUN conda install -c conda-forge coverage flake8 Flask Flask-RESTful imutils dlib opencv numpy pytest requests
RUN pip install -e .

# Run when container is started
ENTRYPOINT ["python", "googlyeyes/server.py"]
EXPOSE 5000
