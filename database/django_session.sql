create table django_session
(
    session_key  varchar(40)              not null
        primary key,
    session_data text                     not null,
    expire_date  timestamp with time zone not null
);

alter table django_session
    owner to rkse;

create index django_session_session_key_c0390e0f_like
    on django_session (session_key varchar_pattern_ops);

create index django_session_expire_date_a5c62663
    on django_session (expire_date);

INSERT INTO public.django_session (session_key, session_data, expire_date) VALUES ('zx2rjwywxf8n5wju0dahus529dvdql2l', '.eJxVjMsOwiAQRf-FtSGUNy7d-w1kYAapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKM7MwmdvrdEuQHtR3gHdqt89zbusyJ7wo_6ODXjvS8HO7fQYVRv7WV4EMxCRKBM7KkSRNoVJiDKAW8dFSE9k6TQufR-qytRGUTmhyKEOz9AQlcOJ8:1qLsPF:_tyd8iw07FMulEeWHqxRB45lZQ9wn6IkSrHuVuFECeU', '2023-08-01 21:38:53.290714 +00:00');
