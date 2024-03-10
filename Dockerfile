# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3

# Install cowsay and fortune
RUN apt-get update && apt-get install -y cowsay fortune

# Configure timezone
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /dbot_app
COPY . /dbot_app

# Creates a non-root user and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN useradd dbotuser && chown -R dbotuser /dbot_app
USER dbotuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "-m", "http.server", "8080"]
CMD ["python", "src/dbot.py"]