BEGIN;


ALTER TABLE IF EXISTS publications DROP CONSTRAINT IF EXISTS style_id;

ALTER TABLE IF EXISTS saved_public DROP CONSTRAINT IF EXISTS user_id;

ALTER TABLE IF EXISTS saved_public DROP CONSTRAINT IF EXISTS public_id;

ALTER TABLE IF EXISTS post_public DROP CONSTRAINT IF EXISTS user_id;

ALTER TABLE IF EXISTS post_public DROP CONSTRAINT IF EXISTS public_id;

ALTER TABLE IF EXISTS comment_public DROP CONSTRAINT IF EXISTS user_id;

ALTER TABLE IF EXISTS comment_public DROP CONSTRAINT IF EXISTS public_id;



DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users
(
    user_id serial,
    login character varying(20) NOT NULL,
    passwd character varying(100) NOT NULL,
    avatar bytea,
    email character varying(100) NOT NULL,
    "time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    CONSTRAINT login UNIQUE (login),
    CONSTRAINT email UNIQUE (email)
);

DROP TABLE IF EXISTS publications;

CREATE TABLE IF NOT EXISTS publications
(
    public_id serial,
    description text,
    style_id integer NOT NULL,
    PRIMARY KEY (public_id)
);

DROP TABLE IF EXISTS styles;

CREATE TABLE IF NOT EXISTS styles
(
    style_id serial,
    style character varying(20) NOT NULL,
    PRIMARY KEY (style_id)
);

DROP TABLE IF EXISTS saved_public;

CREATE TABLE IF NOT EXISTS saved_public
(
    user_id integer,
    public_id integer,
    time_saved timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, public_id)
);

DROP TABLE IF EXISTS post_public;

CREATE TABLE IF NOT EXISTS post_public
(
    user_id integer,
    public_id integer,
    time_public timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, public_id)
);

DROP TABLE IF EXISTS comment_public;

CREATE TABLE IF NOT EXISTS comment_public
(
    user_id integer,
    public_id integer,
    comment text,
    time_comment timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, public_id)
);

ALTER TABLE IF EXISTS publications
    ADD CONSTRAINT style_id FOREIGN KEY (style_id)
    REFERENCES styles (style_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS saved_public
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS saved_public
    ADD CONSTRAINT public_id FOREIGN KEY (public_id)
    REFERENCES publications (public_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS post_public
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS post_public
    ADD CONSTRAINT public_id FOREIGN KEY (public_id)
    REFERENCES publications (public_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS comment_public
    ADD CONSTRAINT user_id FOREIGN KEY (user_id)
    REFERENCES users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS comment_public
    ADD CONSTRAINT public_id FOREIGN KEY (public_id)
    REFERENCES publications (public_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;
