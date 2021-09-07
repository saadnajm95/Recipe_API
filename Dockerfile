
# Load base image : here a python environnement
# We use the slim tag because the image way smaller
# than the classic python image
FROM python:3.8-slim

# Install system dependencies to fix pip install issues
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

# Set the working directory in the container
WORKDIR /usr/src/app

# COPY the project python dependecy list
COPY requirements.txt .

# Install all dependecies from requirements.txt
RUN pip3 install -r requirements.txt

# Install flask globally
RUN pip3 install flask

# COPY source code of the API
COPY . .

# Expose the port 3000 of our container
EXPOSE 3000

# Launch the API on port 3000
CMD [ "flask", "run", "--host=0.0.0.0", "--port=3000"]
