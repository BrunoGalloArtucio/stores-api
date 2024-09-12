FROM python:3.12
# Set work directory into /app folder within docker image 
WORKDIR /app
# We copy requirements.txt and install dependencies before copying the rest of
# the code because Docker caches each line, so we don't have to install all dependencies
# every time a line of code changes
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# second . is current directory (/app)
COPY . . 

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]