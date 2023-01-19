-- Inlead V1 - Database Schema 
--
-- By Josh Ramos (josh-ramos-22)
-- January 2023

create table Players (
    id         serial,
    username   text,
    email      text,
    password   text,
    perms      integer,
    profile_img_url text,

    primary key (id)
);

create table Competitions (
    id                  serial,
    comp_name           text,
    description         text,
    start_time          timestamp not null,
    end_time            timestamp,
    num_games           integer,
    creator             integer not null,
    max_points_per_log  integer,
    is_points_moderated boolean not null,

    primary key (id),
    foreign key (creator) references Players
);

create table CompetitionParticipants (
    player       integer,
    competition  integer,
    is_moderator boolean not null,
    score        integer,

    primary key (player, competition),
    foreign key (player) references Players,
    foreign key (competition) references Competitions

    --constraint valid_score check ((score >= 0))
);

create table PointsRequests (
    id            serial,
    player        integer,
    competition   integer,
    points        integer,

    foreign key (player) references Players,
    foreign key (competition) references Competitions

);

create table Tokens (
    token text,

    primary key (token),
);