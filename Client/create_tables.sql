.open client.db

CREATE TABLE message (
    message_id uniqueidentifier primary key,
    message_time datetime not null,
    content text not null,
    source_user uniqueidentifier not null
);

CREATE TABLE contact (
    contact_id uniqueidentifier primary key,
    username text not null,
    shared_key text not null
);
