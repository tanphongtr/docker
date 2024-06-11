```
mysql -uroot -p

# Truy cập vào mysql1

CREATE USER 'repli1'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'repl1'@'%';
FLUSH PRIVILEGES;
SHOW MASTER STATUS;

# Truy cập vào mysql2
STOP SLAVE;
CHANGE MASTER TO MASTER_HOST='mysql1', MASTER_PORT=3306, MASTER_USER='repl1', MASTER_PASSWORD='password', MASTER_LOG_FILE='binlog.000002', MASTER_LOG_POS=858;
START SLAVE;

-----------------------------
# Truy cập vào mysql2

CREATE USER 'repli2'@'%' IDENTIFIED BY 'password';
GRANT REPLICATION SLAVE ON *.* TO 'repl2'@'%';
FLUSH PRIVILEGES;
SHOW MASTER STATUS;

# Truy cập vào mysql1

CHANGE MASTER TO MASTER_HOST='mysql2', MASTER_PORT=3308, MASTER_USER='repl2', MASTER_PASSWORD='password', MASTER_LOG_FILE='binlog.000002', MASTER_LOG_POS=860;
START SLAVE;


```







```
mariadb -uroot -p

# Truy cập vào mariadb1

CREATE USER 'repli1'@'%' IDENTIFIED BY 'password1';
GRANT REPLICATION SLAVE ON *.* TO 'repl1'@'%';
FLUSH PRIVILEGES;
SHOW MASTER STATUS;

# Truy cập vào mariadb2
STOP SLAVE;
CHANGE MASTER TO MASTER_HOST='mariadb1', MASTER_PORT=3306, MASTER_USER='repl1', MASTER_PASSWORD='password1', MASTER_LOG_FILE='binlog.000002', MASTER_LOG_POS=858;
START SLAVE;

-----------------------------
# Truy cập vào mariadb2

CREATE USER 'repli2'@'%' IDENTIFIED BY 'password2';
GRANT REPLICATION SLAVE ON *.* TO 'repl2'@'%';
FLUSH PRIVILEGES;
SHOW MASTER STATUS;

# Truy cập vào mariadb1

CHANGE MASTER TO MASTER_HOST='host.docker.internal', MASTER_PORT=3308, MASTER_USER='repl2', MASTER_PASSWORD='password2', MASTER_LOG_FILE='binlog.000002', MASTER_LOG_POS=860;
START SLAVE;


```