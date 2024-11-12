# The Docker command FROM specifies the base image for the container
# Our base image is Linux with pre-installed python-3.13
FROM python:3.13

# Set an environment variable
ENV APP_HOME /app

# Set the working directory inside the container
WORKDIR $APP_HOME

# Copy other files to the working directory inside the container
COPY . .

# Install dependencies inside the container
RUN pip install -r requirements.txt

# Expose the port where the application runs inside the container
EXPOSE 3000

# Run our application inside the container
ENTRYPOINT ["python", "main.py"]