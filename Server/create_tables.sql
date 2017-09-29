.open server.db

CREATE TABLE [user] (
   user_id uniqueidentifier primary key,
   salt text not null,
   password text not null
);

CREATE TABLE [message] (
   message_id uniqueidentifier primary key,
   message_date datetime not null,
   target_user uniqueidentifier not null,
   content text not null,
   delievered bit default 0
);
