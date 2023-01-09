-- Inlead V1 - Database Helper Functions
--
-- By Josh Ramos (josh-ramos-22)
-- January 2023

-- Get the leaderboard for the given competition.
create type leaderboard_entry as ( participant text, score integer );
create or replace function
    leaderboard(comp_id integer)
as $$
declare
    _curr leaderboard_entry;
begin
    for _curr in (
        select   p.name, cp.score
        from     Players p
        join     CompetitionParticipants cp on (cp.player = p.id)
        where    cp.competition = comp_id
        order by cp.score desc
    ) loop
        return next _curr
    end loop;
end;
$$ language plpgsql