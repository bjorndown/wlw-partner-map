#!/bin/sh
mkdir -p db

if [ ! -f db/partners.db ]; then
  sqlite3 db/partners.db 'CREATE TABLE "partners" (
    "UUID"	TEXT NOT NULL,
    "zip_code"	INTEGER NOT NULL,
    "status"	TEXT CHECK("status" IN (NULL, "P", "K", "I")),
    "url"	TEXT,
    "comment"	TEXT,
    "canton"	TEXT NOT NULL,
    "district"	TEXT NOT NULL,
    "municipality"	TEXT NOT NULL,
    "partnership_started_at"	TEXT,
    "partnership_cancelled_at"	TEXT,
    "updated_at"	INTEGER,
    PRIMARY KEY("UUID")
  )'
fi;
