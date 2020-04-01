create table votedb.official(
id integer primary key default 1,
email varchar(240) unique not null,
password varchar(120) not null
);

create table votedb.election(
title varchar(255) not null,
election_date DATE not null,
start_time TIME not null,
end_time TIME not null,
primary key (title));
