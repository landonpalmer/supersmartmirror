# Set bas image 3.7
FROM python:3.7

# Set the workikng directory
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# Command to run on container start
CMD ["python", "./main.py"]