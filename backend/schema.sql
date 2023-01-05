-- Inlead V1 - Database Schema 
--
-- By Josh Ramos (josh-ramos-22)
-- January 2023

create table Players {
    id         serial,
    handle_str text,
    email      text,
    password   text,
    perms      integer,
    profile_img_url url,

    primary key id,
    constraint valid_pw check len(password) > 6,
}

create table Competitions {
    id          serial,
    comp_name   text,
    is_complete boolean not null,
    start_time  timestamp not null,
    end_time    timestamp,
    num_games   integer,
    creator     integer not null,
    game_mode   integer,

    primary key (id),
    foreign key creator references Players,

    constraint valid_num_games check num_games >= 0
}

create table CompetitionParticipants {
    player       integer,
    competition  integer,
    is_moderator boolean not null,
    score        integer

    primary key (player, comptetition),
    foreign key player references Players,
    foreign key competition references Competitions,

    constraint valid_score check score >= 0
}

create table PointsRequests {
    player        integer,
    competition   integer,
    points        integer

    primary key (player, comptetition),
    foreign key player references Players,
    foreign key competition references Competitions,

    constraint valid_points check points >= 0
}