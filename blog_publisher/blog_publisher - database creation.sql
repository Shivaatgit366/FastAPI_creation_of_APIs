CREATE DATABASE blog_publisher;


CREATE TABLE authors (
	author_id int NOT NULL AUTO_INCREMENT,
    email varchar(250) NOT NULL,
    password varchar(250) NOT NULL,
    UNIQUE (email),
    PRIMARY KEY (author_id)
);


CREATE TABLE blogs (
	blog_id varchar(6) NOT NULL,
    created_date date NOT NULL,
    author_id int NOT NULL,
    title varchar(1000) NOT NULL,
    body longtext NOT NULL,
    published_date date,
    status ENUM("DRAFT", "PUBLISHED") DEFAULT "DRAFT" NOT NULL,
	PRIMARY KEY (blog_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);
