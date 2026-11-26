# Hyperdrive: texts

Copy for listings, posts and e-mails. Everything here describes what the product does today.

## Taglines

- Your everyday data pipelines, on one small server.
- The self-hosted data platform on SQLite.
- Built for millions of rows, not billions.
- Files and APIs in, clean tables out.

## Short description (about 25 words)

Hyperdrive is a self-hosted data platform on SQLite. It brings in CSV files and REST APIs, turns them into clean typed tables, and delivers them over REST and CSV.

## Medium description (about 60 words)

Hyperdrive does the everyday extract, load and transform work that usually ends up in AWS Glue or Microsoft Fabric. It runs on your own server with Docker Compose or Cloudron and keeps everything in SQLite. Sources, normalisation rules, SQL models, outputs, schedules and authentication are all set up in the browser, and Datasette is included for exploring the data.

## Long description (about 150 words)

Most data work is ordinary: CSV exports, a few REST APIs, some joins, and clean tables for the people and systems that need them. Hyperdrive is a data platform built for exactly that work.

Data comes in as CSV files, as REST APIs pulled on a schedule, or pushed in over REST. Every file and response is kept as it arrived, loaded into a raw table, and normalised into a typed table with clean column names, ISO dates and one row per key. SQL models add joins and aggregates. Any table can then be read over REST as JSON or CSV, written to a scheduled CSV file, or pushed to another system.

Hyperdrive runs on your own server, with Docker Compose or as a Cloudron app, and stores everything in three SQLite files. One backup file holds the whole instance. It suits tables up to some millions of rows.

## Feature blurbs

**Files and APIs in.** CSV with comma or semicolon, with the delimiter and encoding detected. REST APIs pulled on a schedule with paging. JSON or CSV pushed in over REST.

**Normalisation you can see.** Types are detected and can be overridden per column. Decimal commas, local date formats and yes/no values are understood, and a before and after preview shows the result.

**Models in plain SQL.** Save a SELECT as a model, and Hyperdrive keeps the result as a table and rebuilds it after every source run.

**Data out.** Any table as JSON or CSV over REST. Scheduled CSV files. REST pushes to other systems, on a schedule or right after a source has run.

**Authentication in the interface.** API keys for calls into Hyperdrive. Bearer token, basic, API key and OAuth 2.0 client credentials for the calls it makes.

**Runs and schedules.** Cron schedules for sources and outputs, and a run log that shows every step, its rows and its duration.

**Datasette included.** The open-source data explorer reads the same SQLite files, behind the same login.

**Backup and restore.** One file with the data, landing files, configuration and credentials, restored from the interface.

## Limits to state plainly

- Tables up to some millions of rows, not billions. Measured: a 524 MB CSV file with 5.3 million rows loads into raw in 22 seconds and normalises in 103 seconds, using 42 MB of memory.
- Runs execute one at a time.
- Normalised tables are rebuilt in full on each run. There is no incremental mode yet.
- The interface has a single login. There are no per-user roles.

## Boilerplate

Hyperdrive is a self-hosted data platform from Frivold Digital AS. It is built on SQLite and Datasette, and does the everyday extract, load and transform work on a server you control. Contact: thomas.frivold@frivolddigital.com
