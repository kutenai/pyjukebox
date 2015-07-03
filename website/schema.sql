drop table if exists queue;
create table queue (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);