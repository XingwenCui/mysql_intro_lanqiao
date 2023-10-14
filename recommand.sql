-- 创建recommend数据库，mysql中DATABASE和SCHEMA一样
CREATE SCHEMA IF NOT EXISTS recommand;
-- 连接到recommend
USE recommand;

-- Table: user
-- Purpose: 用户表，存储用户名字
CREATE TABLE user (
    id INT PRIMARY KEY, -- id为主键，不能重复
    name VARCHAR(32)    -- 用户名，VARCHAR为可变长度
);

-- Table: anime
-- Purpose: 番剧表，存储番剧名字和简介
CREATE TABLE anime (
    id INT PRIMARY KEY, -- id为主键
    name VARCHAR(128),  -- 番剧名
    brief VARCHAR(128)  -- 简介
);

-- Table: anime_style
-- Purpose: 番剧 - 标签表，存储番剧及其对应的标签的 ID
CREATE TABLE user_anime (
    user_id INT,
    anime_id INT,
    FOREIGN KEY(user_id) REFERENCES user(id),   -- user_id是user table中的，与id关联
    FOREIGN KEY(anime_id) REFERENCES anime(id)
);

-- TABLE: user_anime
-- Purpose: 用户 - 番剧表，记录用户已经看过并喜欢的番剧的 ID
CREATE TABLE anime_style (
    anime_id INT,
    style_id INT,
    FOREIGN KEY(anime_id) REFERENCES anime(id)
);


-- 向4个table中插入数据
INSERT INTO user VALUE 
(1, 'Shiyanlou');

INSERT INTO anime VALUE
(279,"a","A"),
(3494,"b","B"),
(3377,"c","C"),
(3452,"d","D"),
(782,"e","E"),
(3421,"f","F"),
(2730,"g","G");

INSERT INTO user_anime VALUE
(1, 782),       -- 可以发现，插入的id只能是user中存在的id=1，不能是2，这就是外键的作用
(1, 3421),
(1, 2730);

INSERT INTO anime_style VALUE
(279,26),
(279,30),
(279,32),
(279,8),
(279,7),
(3494,9),
(3494,1),
(3494,2),
(3494,4),
(3377,34),
(3377,7),
(3377,18),
(3452,30),
(3452,32),
(3452,7),
(3452,22),
(782,30),
(782,32),
(782,7),
(782,1),
(782,50),
(3421,30),
(3421,32),
(3421,7),
(3421,22),
(2730,11),
(2730,30),
(2730,22);