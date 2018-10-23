# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY Pipfile* /app/

# Install any needed packages specified in requirements.txt
RUN pip3 install pipenv
RUN pipenv install --system --deploy --verbose

# Make port 80 available to the world outside this container
EXPOSE 5000
COPY . /app

# Define environment variable
ENV FLASK_APP=api.py

# Run app.py when the container launches
CMD ["flask", "run"]
