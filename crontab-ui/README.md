# On Ubuntu, it can look something like this and /etc/cron.d/root is used
```shell
docker run -d -p 8000:8000 -v /etc/cron.d:/etc/crontabs alseambusher/crontab-ui
```

# Install NVM
```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```
```
nvm install 16
nvm use 16
```
