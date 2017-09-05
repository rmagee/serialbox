CREATE ROLE cerealkiller LOGIN
  UNENCRYPTED PASSWORD 'StopMakingSense'
  NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
CREATE DATABASE serialbox
  WITH OWNER = cerealkiller
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;
COMMENT ON DATABASE serialbox
  IS 'default administrative connection database';
\connect serialbox


