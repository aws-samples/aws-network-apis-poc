FROM public.ecr.aws/lambda/python:3.8

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install -r requirements.txt

# define the port number the container should expose
EXPOSE 80

# run the command
ENTRYPOINT ["python", "./app.py"]
