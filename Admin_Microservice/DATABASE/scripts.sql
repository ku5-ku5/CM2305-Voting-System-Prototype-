create table votedb.official(
id integer primary key default 1,
email varchar(240) unique not null,
password varchar(120) not null
);

create table votedb.election(
title varchar(60) primary key,
candidate1 varchar(60),
candidate2 varchar(60),
candidate3 varchar(60));
