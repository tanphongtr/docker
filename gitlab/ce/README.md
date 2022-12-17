docker-compose.yml
```yml
web:
  image: 'gitlab/gitlab-ce:latest'
  restart: always
  hostname: 'gitlab-example.com'
  environment:
    GITLAB_OMNIBUS_CONFIG: |
      external_url 'http://gitlab-example.com'
  ports:
    - '9510:80'
    - '4443:443'
    - '2222:22'

  volumes:
    - '${GITLAB_HOME}/config:/etc/gitlab'
    - '${GITLAB_HOME}/logs:/var/log/gitlab'
    - '${GITLAB_HOME}/data:/var/opt/gitlab'
    - '${GITLAB_HOME}/config/ssl:/etc/gitlab/ssl'
```

Root User:
```
root
Password in ${GITLAB_HOME}/config/initial_root_password
```

![image](https://user-images.githubusercontent.com/11567406/208229803-23f576d9-38fe-4986-a0b0-d014d34d59bb.png)

