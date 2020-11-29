-- Your SQL goes here
CREATE TABLE "links" (
	"shortlink"	TEXT NOT NULL UNIQUE,
	"url"	TEXT NOT NULL,
	PRIMARY KEY("shortlink")
);