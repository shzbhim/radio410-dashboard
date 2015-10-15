drop table if exists user;
create table user (
  id integer primary key autoincrement,
  username text not null,
  pw_hash text not null
);

drop table if exists announcement;
create table announcement (
  id integer primary key autoincrement,
--author_id integer not null,
  text text not null,
  pub_date integer
);

--drop table if exists broadcast;
--create table broadcast (
--  id integer primary key autoincrement,
--  text text not null,
--  broadcast_url text not null,
--  download_url text not null,
--  pub_date integer
--);
