.open client.db

CREATE TABLE message (
    message_time datetime not null,
    content text not null,
    source_user text not null,
    target_user text not null

);

CREATE TABLE contact (
    username text not null,
    shared_key text not null
);
