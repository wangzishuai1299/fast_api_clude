CREATE DATABASE IF NOT EXISTS admin_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE admin_db;

-- 作者表 author
CREATE TABLE IF NOT EXISTS author (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    discription VARCHAR(100) NOT NULL,
    INDEX idx_name (name),
    INDEX idx_discription (discription)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 初始化种子数据，INSERT IGNORE：存在就跳过，不会主键冲突
INSERT IGNORE INTO author (name, discription) VALUES
('鲁迅', '近代文学作家'),
('老舍', '现代小说家');

-- 书籍表 book，外键关联 author.id
CREATE TABLE IF NOT EXISTS book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(30) NOT NULL,
    author_id INT NOT NULL,
    price INT NOT NULL,
    INDEX idx_title (title),
    INDEX idx_author_id (author_id),
    FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 种子书籍数据
INSERT IGNORE INTO book (title, author_id, price) VALUES
('呐喊', 1, 39),
('骆驼祥子', 2, 42);
