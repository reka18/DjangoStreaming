create table user_manager_user
(
    id    bigint generated by default as identity
        primary key,
    name  varchar(200) not null
        unique,
    dob   date         not null,
    age   integer      not null,
    email varchar(254) not null
);

alter table user_manager_user
    owner to rkse;

create index user_manager_user_name_ee403952_like
    on user_manager_user (name varchar_pattern_ops);

INSERT INTO public.user_manager_user (id, name, dob, age, email) VALUES (2, 'Apple', '2023-07-18', 1, 'apple@qtvly.com');
INSERT INTO public.user_manager_user (id, name, dob, age, email) VALUES (3, 'Banana', '2023-07-18', 1, 'banana@qtivly.com');
