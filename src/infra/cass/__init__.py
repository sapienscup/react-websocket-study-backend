# CREATE TYPE software_world.complete_name (
#     first_name TEXT,
#     last_name TEXT
# );

# CREATE TABLE software_world.developers_by_language(
#     id UUID,
#     email TEXT,
#     programming_language TEXT,
#     name FROZEN<complete_name>,
#     PRIMARY KEY((programming_language), id)
# );

# INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (c9227684-2db5-5690-b85f-14ee774d11d4, 'sejaehu@bisvod.ws', 'maybe', { first_name: 'Alberta', last_name: 'Paul' });
# INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (41bf775a-c09d-5746-8203-f50e9f456c66, 'muelo@wiizuul.bz', 'seat', { first_name: 'Ann', last_name: 'Ruiz' });
# INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (fc48f3ef-28a2-5421-b52a-0833a14d0636, 'sikozova@vicecpob.rw', 'land', { first_name: 'Ivan', last_name: 'Watts' });
# INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (bb3d6ff6-6cc8-5f88-a938-d468a8d486b2, 'sa@tu.pk', 'describe', { first_name: 'Brett', last_name: 'Cox' });
# INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (0ac466bc-84ea-57d9-9feb-4959e137211a, 'danmusvo@tenluk.vg', 'dance', { first_name: 'Ethel', last_name: 'Fleming' });
# INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (6b653b15-fb96-5d7a-8059-3ad9f14ef35d, 'gac@fag.au', 'airplane', { first_name: 'Victoria', last_name: 'Marshall' });
# INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (efdc7b5c-a8f2-505e-a455-1196dee47859, 'tusib@ja.eh', 'brother', { first_name: 'Josie', last_name: 'Wright' });
# INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (8ce4b0f4-455b-58e1-927a-3975f6c90405, 'cezu@pa.ht', 'trade', { first_name: 'Lizzie', last_name: 'Stokes' });
