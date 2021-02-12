create table cpu_usage
(
    id          bigint auto_increment
        primary key,
    timestamp   timestamp default current_timestamp() not null,
    cpu_percent float                                 null
);

create table disk_usage
(
    id             bigint auto_increment
        primary key,
    disk_path      varchar(255)                          null,
    disk_total     bigint                                null,
    disk_used      bigint(30)                            null,
    percent_used   float                                 null,
    disk_name      varchar(255)                          null,
    readable_total varchar(20)                           null,
    readable_used  varchar(20)                           null,
    timestamp      timestamp default current_timestamp() not null
);

create table memory_usage
(
    id                bigint auto_increment
        primary key,
    timestamp         timestamp default current_timestamp() not null,
    total_memory      bigint                                null,
    used_memory       bigint                                null,
    percent_used      double                                null,
    memory_total_read varchar(20)                           null,
    memory_used_read  varchar(20)                           null
);

create table net_io_counter
(
    id                bigint auto_increment
        primary key,
    timestamp         timestamp default current_timestamp() not null,
    host              varchar(50)                           null,
    nic               varchar(50)                           null,
    bytes_sent        bigint                                null,
    bytes_received    bigint                                null,
    readable_sent     varchar(20)                           null,
    readable_received varchar(20)                           null
);

create table table_name
(
    column_1 int not null
        primary key
);


