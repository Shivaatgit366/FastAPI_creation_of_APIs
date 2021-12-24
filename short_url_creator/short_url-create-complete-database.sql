CREATE DATABASE url_shortener;


CREATE TABLE users (
    user_id int NOT NULL AUTO_INCREMENT,
    email varchar(250) NOT NULL,
    password varchar(250) NOT NULL,
    PRIMARY KEY (user_id)
);


CREATE TABLE short_urls (
	created_date date NOT NULL,
    user_id int NOT NULL,
    original_url varchar(1000) NOT NULL,
    short_url varchar(6) NOT NULL,
    PRIMARY KEY (short_url),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


CREATE TABLE clicks (
	date date NOT NULL,
    short_url varchar(6) NOT NULL,
    click_count int NOT NULL,
    PRIMARY KEY (date, short_url),
    FOREIGN KEY (short_url) REFERENCES short_urls(short_url)
);


SELECT created_date,
	   user_id,
	   COUNT(short_url) AS number_of_urls_converted
FROM short_urls
GROUP BY user_id, created_date;


UPDATE clicks
SET click_count = click_count + 1
WHERE conditions;