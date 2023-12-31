create table conversation_manager_message
(
    id           integer generated by default as identity
        primary key,
    text         varchar(260)             not null,
    created_at   timestamp with time zone not null,
    visible      boolean                  not null,
    up_votes     integer                  not null,
    down_votes   integer                  not null,
    recipient_id bigint                   not null
        constraint conversation_manager_recipient_id_eea4bf75_fk_user_mana
            references user_manager_user
            deferrable initially deferred,
    sender_id    bigint                   not null
        constraint conversation_manager_sender_id_badb79e0_fk_user_mana
            references user_manager_user
            deferrable initially deferred
);

alter table conversation_manager_message
    owner to rkse;

create index conversation_manager_message_recipient_id_eea4bf75
    on conversation_manager_message (recipient_id);

create index conversation_manager_message_sender_id_badb79e0
    on conversation_manager_message (sender_id);

INSERT INTO public.conversation_manager_message (id, text, created_at, visible, up_votes, down_votes, recipient_id, sender_id) VALUES (1, 'How are you?', '2023-07-18 21:45:56.000000 +00:00', true, 0, 0, 3, 2);
