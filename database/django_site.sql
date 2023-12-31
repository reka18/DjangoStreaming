create table django_site
(
    id     integer generated by default as identity
        primary key,
    domain varchar(100) not null
        constraint django_site_domain_a2e37b91_uniq
            unique,
    name   varchar(50)  not null
);

alter table django_site
    owner to rkse;

create index django_site_domain_a2e37b91_like
    on django_site (domain varchar_pattern_ops);

INSERT INTO public.django_site (id, domain, name) VALUES (1, 'example.com', 'example.com');
