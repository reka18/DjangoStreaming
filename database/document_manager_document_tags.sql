create table document_manager_document_tags
(
    id          bigint generated by default as identity
        primary key,
    document_id integer not null
        constraint document_manager_doc_document_id_e3e11974_fk_document_
            references document_manager_document
            deferrable initially deferred,
    tag_id      integer not null
        constraint document_manager_doc_tag_id_018bb98d_fk_tag_manag
            references tag_manager_tag
            deferrable initially deferred,
    constraint document_manager_document_tags_document_id_tag_id_d8614d0c_uniq
        unique (document_id, tag_id)
);

alter table document_manager_document_tags
    owner to rkse;

create index document_manager_document_tags_document_id_e3e11974
    on document_manager_document_tags (document_id);

create index document_manager_document_tags_tag_id_018bb98d
    on document_manager_document_tags (tag_id);

