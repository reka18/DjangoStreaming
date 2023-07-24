create table auth_group
(
    id   integer generated by default as identity
        primary key,
    name varchar(150) not null
        unique
);

alter table auth_group
    owner to rkse;

create index auth_group_name_a6ea08ec_like
    on auth_group (name varchar_pattern_ops);

