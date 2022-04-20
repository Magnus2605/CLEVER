SELECT * FROM cleverapp.charging_stations;
SELECT * FROM cleverapp.address;
SET SQL_SAFE_UPDATES = 0; -- Gør at vi kan ændre i tabel

-- Indledningsvis har vi importeret den .csv fil vi har fået udleveret via import funktion.

-- Vi opdatere data, således at det er nemmere at læse.
UPDATE cleverapp.charging_stations SET LocationName = REPLACE (LocationName, 'Ã…', 'Aa');
UPDATE cleverapp.charging_stations SET LocationName = REPLACE (LocationName, 'Ã¥', 'aa');
UPDATE cleverapp.charging_stations SET LocationName = REPLACE (LocationName, 'Ã¸', 'oe');
UPDATE cleverapp.charging_stations SET LocationName = REPLACE (LocationName, 'Ã¦', 'ae');
UPDATE cleverapp.charging_stations SET LocationName = REPLACE (LocationName, 'Ã†', 'Ae');
UPDATE cleverapp.charging_stations SET LocationName = REPLACE (LocationName, 'Ã©', 'e');
UPDATE cleverapp.charging_stations SET LocationName = REPLACE (LocationName, 'Ã˜', 'oe');
UPDATE cleverapp.charging_stations SET StreetName = REPLACE (StreetName, 'Ã…', 'Aa');
UPDATE cleverapp.charging_stations SET StreetName = REPLACE (StreetName, 'Ã¥', 'aa');
UPDATE cleverapp.charging_stations SET StreetName = REPLACE (StreetName, 'Ã¸', 'oe');
UPDATE cleverapp.charging_stations SET StreetName = REPLACE (StreetName, 'Ã¦', 'ae');
UPDATE cleverapp.charging_stations SET StreetName = REPLACE (StreetName, 'Ã†', 'Ae');
UPDATE cleverapp.charging_stations SET StreetName = REPLACE (StreetName, 'Ã©', 'e');
UPDATE cleverapp.charging_stations SET StreetName = REPLACE (StreetName, 'Ã˜', 'oe');
UPDATE cleverapp.charging_stations SET City = REPLACE (City, 'Ã…', 'Aa');
UPDATE cleverapp.charging_stations SET City = REPLACE (City, 'Ã¥', 'aa');
UPDATE cleverapp.charging_stations SET City = REPLACE (City, 'Ã¸', 'oe');
UPDATE cleverapp.charging_stations SET City = REPLACE (City, 'Ã¦', 'ae');
UPDATE cleverapp.charging_stations SET City = REPLACE (City, 'Ã†', 'Ae');
UPDATE cleverapp.charging_stations SET City = REPLACE (City, 'Ã©', 'e');
UPDATE cleverapp.charging_stations SET City = REPLACE (City, 'Ã˜', 'oe');

-- Vi sørger for at alt starter med stort bogstav
UPDATE cleverapp.charging_stations SET LocationName = CONCAT(UCASE(LEFT(LocationName, 1)), SUBSTRING(LocationName, 2));
UPDATE cleverapp.charging_stations SET StreetName = CONCAT(UCASE(LEFT(StreetName, 1)), SUBSTRING(StreetName, 2));
UPDATE cleverapp.charging_stations SET City = CONCAT(UCASE(LEFT(City, 1)), SUBSTRING(City, 2));

-- Vi sletter kollonner der ikke har relation til adresse for at opfylde normalisation
ALTER TABLE cleverapp.charging_stations DROP COLUMN Accessibility;
ALTER TABLE cleverapp.charging_stations DROP COLUMN ConnectorCount;
ALTER TABLE cleverapp.charging_stations DROP COLUMN Capacity;
ALTER TABLE cleverapp.charging_stations DROP COLUMN ConnectorVariantName;

-- Vi giver tabellen et navn der passer overens med data.
ALTER TABLE cleverapp.charging_stations RENAME TO cleverapp.address;
-- Vi laver en autoincrement funktion, der gør at vi kan få en primærnøgle per række.

-- vi laver en ny tabel via det indbyggede tabelkonstruktionsværktøj 
-- Vi giver tabellen navnet charging_types, da den viser de forskellige ladetyper.
-- Ved at gøre brug af distinct i den originale .csv fil er det muligt at kende de forskellige ladetyper.
-- Vi indsætter de forskellige ladetyper, samt et id nr som fungerer som primærnøgle.
insert into cleverapp.charging_types values (1,"IEC Type 1");
insert into cleverapp.charging_types values (2,"IEC Type 2");
insert into cleverapp.charging_types values (3,"CCS");
insert into cleverapp.charging_types values (4,"CHAdeMO");



-- evstats kommer fra https://www.reddit.com/r/electricvehicles/comments/o53ynn/the_big_ev_spreadsheet/
-- evstats er en tabel over bilmærker og batterikapacitet. Den bruges til at beregne ladehastighed.

-- Import af .csv igen for at isolere ladetype, ladeeffekt og ladeantal.
-- 
SELECT * FROM cleverapp.charging_stations;
ALTER TABLE cleverapp.charging_stations DROP COLUMN ï»¿Accessibility;
ALTER TABLE cleverapp.charging_stations DROP COLUMN LocationName;
ALTER TABLE cleverapp.charging_stations DROP COLUMN Latitude;
ALTER TABLE cleverapp.charging_stations DROP COLUMN Longitude;
ALTER TABLE cleverapp.charging_stations DROP COLUMN StreetName;
ALTER TABLE cleverapp.charging_stations DROP COLUMN HouseNumber;
ALTER TABLE cleverapp.charging_stations DROP COLUMN PostalCode;
ALTER TABLE cleverapp.charging_stations DROP COLUMN City;
ALTER TABLE cleverapp.charging_stations RENAME TO cleverapp.charging_type_list; 
SELECT * FROM cleverapp.charging_type_list;
-- 

-- Vi tilføjer et ConnectorVariantNameId således vi kan bruge en foreign key fra charging_types. på denne måde for typen af ladestander et id.
ALTER TABLE `cleverapp`.`charging_type_list` 
ADD COLUMN `ConnectorVariantNameId` INT NOT NULL AFTER `ChargingStationId`,
CHANGE COLUMN `ConnectorVariantName` `ConnectorVariantName` TEXT NULL DEFAULT NULL AFTER `ConnectorVariantNameId`;

-- Opdater tabellen så ladetype id kommer over i charging_type_list.
UPDATE cleverapp.charging_type_list 
  INNER JOIN cleverapp.charging_types
  ON cleverapp.charging_type_list.ConnectorVariantName = cleverapp.charging_types.ConnectorVariantName
  SET cleverapp.charging_type_list.ConnectorVariantNameId = cleverapp.charging_types.idCharging_types;
  


-- Vi laver en tabel der viser hvor meget det koster at parkere over tid og indsætter values i form af gebyre og minutter.
insert into cleverapp.parking_fees values ("1","45","15");
insert into cleverapp.parking_fees values ("2","90","30");
insert into cleverapp.parking_fees values ("3","135","45");
insert into cleverapp.parking_fees values ("4","180","60");
insert into cleverapp.parking_fees values ("5","285","75");
insert into cleverapp.parking_fees values ("6","390","90");
insert into cleverapp.parking_fees values ("7","495","105");
insert into cleverapp.parking_fees values ("8","600","120");
insert into cleverapp.parking_fees values ("9","750","135");
insert into cleverapp.parking_fees values ("10","900","150");
insert into cleverapp.parking_fees values ("11","1050","165");

-- evstats er hentet fra denne side https://www.reddit.com/r/electricvehicles/comments/o53ynn/the_big_ev_spreadsheet/
-- evstats er en tabel over køretøjer og deres ladekapacitet. Dataen bruges til at beregne ladetid.

-- PÅ GRUND AF MANGEL PÅ TILLADELSE HAR VI IKKE KUNNE OPSTILLE FOREIGN KEYS.