# NOTES

urllib.parse.quote_plus("P@$$w0rd").replace("%", "%%")

## Override SQLAlchemy URL

from urllib.parse import quote_plus

URL_encode_Password = quote_plus(settings.POSTGRES_PASSWORD).replace("%", "%%")  # URL-encode the password for handling special characters

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.POSTGRES_USER}:{URL_encode_Password}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

## Set Postman to save bearer token to environment variable

pm.environment.set("JWT", pm.response.json().access_token);

## Working on Production Server

## Configuring Custom SSH Key to Access Vagrant Machine

```bash
cat ~/.ssh/id_ed25519.pub | ssh -i ./Vagrant/.vagrant/machines/default/virtualbox/private_key vagrant@192.168.73.10 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

## System Update and Python Installation

```bash
sudo apt update && sudo apt upgrade -y
python3 --version

# Install Python 3.13
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.13 -y
python3.13 --version
python3.13 -m ensurepip --upgrade
sudo apt install python3-pip -y
sudo pip3 install virtualenv
```

## Install and Configure PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib -y
psql --version
psql --help
psql -U postgres
```

### Resolving PostgreSQL Peer Authentication Issue

```bash
# For solving PostgreSQL peer authentication issue on Ubuntu
su - postgres
psql -U postgres
\password postgres
\q
exit

cd /etc/postgresql/16/main
sudo vim postgresql.conf   
    listen_addresses = '*'

sudo vim pg_hba.conf
    peer => md5
    ipv4   0.0.0.0/0
    ipv6   ::/0

# Database administrative login by Unix domain socket
local   all             postgres                                md5

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     md5
# IPv4 local connections:
host    all             all             0.0.0.0/0               md5
# IPv6 local connections:
host    all             all             ::/0                    md5
```

### Restart PostgreSQL Service

```bash
sudo systemctl restart postgresql
```

### Connect Remotely or Locally with the Root User

```bash
psql -U postgres
```

### Create a New User for the App

```bash
sudo adduser fastapi
sudo usermod -aG sudo fastapi
```

## Managing Python Environment Using UV Package Manager

**Install UV Package Manager**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Enable UV Shell Auto Completion

**Determine your shell (e.g., with `echo $SHELL`), then run one of:**

```bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
echo 'uv generate-shell-completion fish | source' >> ~/.config/fish/config.fish
echo 'eval (uv generate-shell-completion elvish | slurp)' >> ~/.elvish/rc.elv

echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bashrc
echo 'eval "$(uvx --generate-shell-completion zsh)"' >> ~/.zshrc
echo 'uvx --generate-shell-completion fish | source' >> ~/.config/fish/config.fish
echo 'eval (uvx --generate-shell-completion elvish | slurp)' >> ~/.elvish/rc.elv
```

### Manage Python Versions and Dependencies

```bash
uv python list --only-installed
uv python install 3.13
uv python list --only-installed
uv venv -p 3.13
uv pip sync requirements.lock
```

### Update Requirements

```bash
uv pip install -r requirements.txt
```

### If You Update Requirements

```bash
pip freeze > requirements.txt
uv pip compile requirements.txt --output-file requirements.lock
```

### Run the App

- Note: This will give an error because we need to create the database first and update the environment variables

```bash
uvicorn app.main:app --reload
```

- Settin the environment variables manualy

export DATABASE_HOSTNAME=localhost
export DATABASE_PORT=5432
export DATABASE_NAME=social-media-db
export DATABASE_USERNAME=postgres
export DATABASE_PASSWORD=Daf28876#@
export SECRET_KEY=655d041f3ef4b80d43bd74e14cc47c17b459ac0d88787cbd85625dexport be8583186b
export ALGORITHM=HS256
export ACCESS_TOKEN_EXPIRE_MINUTES=60