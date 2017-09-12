# Fabric

Fabric is a Python library and command-line tool for streamlining the use of SSH for application deployment or systems administration tasks.

For SSH it relays on python library paramiko.

# Versions
* Original, only for Python2 at the moment: http://www.fabfile.org/ (available at OpenSUSE Leap 42.3 as python-fabric)
* Fork with Python3 support: https://pypi.python.org/pypi/Fabric3 (available using pip)

# Setup

## Optional: load id_rsa_insecure to your ssh-agent

Please note that if you do not do it, you will need to add -i ./id_rsa_insecure to the fab commands

## Containers to run examples:
```
## Create a network so interal DNS is enabled at docker (we do not want to touch default network)

docker network create mynetwork

## Direct access
docker run -d --name centos6-ssh-1 --network mynetwork -p 2020:22 jdeathe/centos-ssh:centos-6
docker run -d --name centos6-ssh-2 --network mynetwork -p 2021:22 jdeathe/centos-ssh:centos-6
docker run -d --name centos7-ssh-1 --network mynetwork -p 2022:22 jdeathe/centos-ssh:centos-7
docker run -d --name centos7-ssh-2 --network mynetwork -p 2023:22 jdeathe/centos-ssh:centos-7

## Indirect access
docker run -d --name centos7-ssh-indirect --network mynetwork jdeathe/centos-ssh:centos-7
docker run -d --name centos7-ssh-gateway --network mynetwork -p 2024:22 jdeathe/centos-ssh:centos-7

## Allow app-admin to use sudo without password
docker exec -t -i centos6-ssh-1  bash -c "echo 'app-admin        ALL=(ALL)       NOPASSWD: ALL' > /etc/sudoers.d/app-admin"
docker exec -t -i centos6-ssh-2  bash -c "echo 'app-admin        ALL=(ALL)       NOPASSWD: ALL' > /etc/sudoers.d/app-admin"
docker exec -t -i centos7-ssh-1  bash -c "echo 'app-admin        ALL=(ALL)       NOPASSWD: ALL' > /etc/sudoers.d/app-admin"
docker exec -t -i centos7-ssh-2  bash -c "echo 'app-admin        ALL=(ALL)       NOPASSWD: ALL' > /etc/sudoers.d/app-admin"
docker exec -t -i centos7-ssh-indirect  bash -c "echo 'app-admin        ALL=(ALL)       NOPASSWD: ALL' > /etc/sudoers.d/app-admin"
docker exec -t -i centos7-ssh-gateway  bash -c "echo 'app-admin        ALL=(ALL)       NOPASSWD: ALL' > /etc/sudoers.d/app-admin"
```

# Containers with direct access

## Get uname -a for all containers (manual)
```
fab -H app-admin@localhost:2020,app-admin@localhost:2021,app-admin@localhost:2022,app-admin@localhost:2023 -- 'uname -a'
```

## Get uname -a for all containers (task)
```
fab -H app-admin@localhost:2020,app-admin@localhost:2021,app-admin@localhost:2022,app-admin@localhost:2023 mytasks.uname
```

## Show /etc/redhat-release for all containers
```
fab -H app-admin@localhost:2020,app-admin@localhost:2021,app-admin@localhost:2022,app-admin@localhost:2023 mytasks.cat_file:file_path=/etc/redhat-release
```

## Show /etc/redhat-release for all containers (in parallel)
```
fab -P -H app-admin@localhost:2020,app-admin@localhost:2021,app-admin@localhost:2022,app-admin@localhost:2023 mytasks.cat_file:file_path=/etc/redhat-release
```

## Show /etc/shadow for all containers

```
fab -H app-admin@localhost:2020,app-admin@localhost:2021,app-admin@localhost:2022,app-admin@localhost:2023 mytasks.cat_file:file_path=/etc/shadow,use_sudo=True
```

## Get a prompt requesting a file path, and show file contents

When asked for a file path, type '/etc/redhat-release'.

```
fab -H app-admin@localhost:2020 mytasks.cat_file
```



## Fetching local user
```
fab mytasks.local_user

```

## Fetching the account ID for an AWS account

You need either a ~/.boto file or export the path to the boto credentials file.
```
fab mytasks.get_account_id
```

# Indirect access

## Running a command
```
fab -g app-admin@localhost:2024 -H app-admin@centos7-ssh-indirect -- 'uname -a'
```

## Running a task
```
fab -g app-admin@localhost:2024 -H app-admin@centos7-ssh-indirect mytasks.cat_file:file_path=/etc/redhat-release
```
