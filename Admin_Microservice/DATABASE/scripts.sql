create table votedb.official (
officialuid integer primary key auto_increment,
firstname char(50) not null,
surname char(50) not null,
email varchar(240) not null unique,
password varchar(255) not null
);

create table votedb.election(
title varchar(255) not null,
election_date DATE not null,
start_time TIME not null,
end_time TIME not null,
primary key (title));
