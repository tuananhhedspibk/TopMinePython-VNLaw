select * from article_topics;
select * from topics;

delete from topics;

drop table topics;
drop table article_topics;

GRANT ALL PRIVILEGES ON TABLE article_topics_id_seq TO anhtt;
GRANT ALL PRIVILEGES ON TABLE topics TO anhtt;

create table topics (
  id integer primary key,
  value text
);

create table article_topics (
  id serial,
  article_id integer,
  topic_id integer REFERENCES topics(id)
);