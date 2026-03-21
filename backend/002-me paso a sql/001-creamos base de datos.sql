sudo mysql -u root -p
CREATE DATABASE IF NOT EXISTS flomvidex;
USE flomvidex;

-- Tabla 1: Tracks (Todas las canciones viven aquí)
CREATE TABLE tracks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT NOT NULL,
    file TEXT NOT NULL,
    artist VARCHAR(100),
    tags TEXT,
    dir VARCHAR(100) NOT NULL
);

-- Tabla 2: Logs (Para registrar qué hace el Admin)
CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla 3: Backups (Para registrar cuándo se hacen las copias de seguridad)
CREATE TABLE backups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tu usuario seguro
CREATE USER IF NOT EXISTS 'dj_maidcore'@'localhost' IDENTIFIED BY 'dj_maidcore';

GRANT USAGE ON *.* TO 'dj_maidcore'@'localhost';
ALTER USER 'dj_maidcore'@'localhost' 
REQUIRE NONE 
WITH MAX_QUERIES_PER_HOUR 0 
MAX_CONNECTIONS_PER_HOUR 0 
MAX_UPDATES_PER_HOUR 0 
MAX_USER_CONNECTIONS 0;

GRANT ALL PRIVILEGES ON flomvidex.* TO 'dj_maidcore'@'localhost';

FLUSH PRIVILEGES;
