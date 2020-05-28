SELECT title FROM movies
JOIN stars ON movies.id = stars.movie_id
WHERE stars.person_id == (SELECT id FROM people WHERE name == "Johnny Depp")
OR stars.person_id == (SELECT id FROM people WHERE name == "Helena Bonham Carter")
GROUP BY title
HAVING COUNT(*) > 1;