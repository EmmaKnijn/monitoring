CREATE DATABASE IF NOT EXISTS system_stats;
USE system_stats;

CREATE TABLE IF NOT EXISTS stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hostname VARCHAR(255) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    disk_usage FLOAT NOT NULL,
    cpu_usage FLOAT NOT NULL,
    ram_usage FLOAT NOT NULL,
    network_sent BIGINT NOT NULL,
    network_recv BIGINT NOT NULL
);