The TCA-Assignment-Planner is a tool designed to automate the process of assignement planning for a clan in the game Runescape.

This project was chosen to automate a long tedious task, therefore saving time for multiple clan administrators and removing human error.
The project uses the following technological features:

- Makes calls to the Runescape API
- Database CRUD operations
- Generates output CSV files
- Skill assignment alogrithm
- Handles multiple edgecases
- Custom string formatting
- Custom data structues

The software takes a list of members, where a call to the Runescape-API will be made once per user to get a list of skill statistics.
In order to save on repeated API calls and to quickly reaccess important information, a SQLite database is used to track the data.
The database was implemented using multiple tables and handles all operatings of CRUD.

The output for this software is 2 different csv files;
The first csv output file gives a concise report on whether members met their main and optional assignments set from the previous month.
This is done by comparing the data from the recent API call, to the data from the previous month stored in the database.
The second csv output file gives a list of formatted string - ready to be copy and pasted straight into the clan forum without any further editing.
Within this formatted string, it contains information on the player, the new main assignment and the new optional assignment.

The selection of main assignments comes from an algorithm taking the following factors into account:
- Whether the user is a Free to play or Pay to play member (reduced skill selection for FTP members)
- Will not assign the same skill for both the main and optional assignment
- Excludes certain skills from selection
- Will not assign any skills used in the previous month
- Players with skill levels under 65 will be given a whole level target, rather than a 50000 xp target

- The order of assignment for eligible skills is as follows:
- Any skill under level 99
- If no skills left under 99, look for lowest 120 cap skill
- If all skills are maxed, pick the skill with lowest xp
