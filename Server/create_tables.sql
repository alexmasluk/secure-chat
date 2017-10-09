.open server.db

CREATE TABLE [user] (
    salt text not null,
    password text not null,
    username text not null,
    publickey text not null
);

CREATE TABLE [message] (
    message_date datetime not null,
    target_user uniqueidentifier not null,
    content text not null,
    delivered bit default 0
);
