use yukiyu;

DROP TABLE IF EXISTS comment;

CREATE TABLE comment(
    comment_id int NOT NULL AUTO_INCREMENT primary key,
    name varchar(20) not null,
    info text not null,
    date datetime not null,
    bangumi_id int not null,
    likes int not null    
)engine=innodb default charset=utf8mb4;

INSERT INTO comment VALUES (1,'ztzdr','好','2022-01-01 11:11:11',2262592,100);
INSERT INTO comment VALUES (2,'ztzdr','xing','2022-01-01 11:11:12',2262592,10);
INSERT INTO comment VALUES (3,'ztzdr','大魔王不好看','2022-01-01 11:11:14',2262592,1);
INSERT INTO comment VALUES (4,'ztzdr','不喜欢沙优的人有难了','2022-01-01 11:11:14',6820713,1000);
