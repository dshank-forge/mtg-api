--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: david
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO david;

--
-- Name: cards; Type: TABLE; Schema: public; Owner: david
--

CREATE TABLE public.cards (
    id integer NOT NULL,
    name character varying NOT NULL,
    type character varying NOT NULL,
    colors character varying,
    cmc integer
);


ALTER TABLE public.cards OWNER TO david;

--
-- Name: cards_id_seq; Type: SEQUENCE; Schema: public; Owner: david
--

CREATE SEQUENCE public.cards_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cards_id_seq OWNER TO david;

--
-- Name: cards_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: david
--

ALTER SEQUENCE public.cards_id_seq OWNED BY public.cards.id;


--
-- Name: decks; Type: TABLE; Schema: public; Owner: david
--

CREATE TABLE public.decks (
    id integer NOT NULL,
    title character varying NOT NULL,
    format character varying,
    colors character varying,
    creator character varying
);


ALTER TABLE public.decks OWNER TO david;

--
-- Name: decks_id_seq; Type: SEQUENCE; Schema: public; Owner: david
--

CREATE SEQUENCE public.decks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.decks_id_seq OWNER TO david;

--
-- Name: decks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: david
--

ALTER SEQUENCE public.decks_id_seq OWNED BY public.decks.id;


--
-- Name: cards id; Type: DEFAULT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.cards ALTER COLUMN id SET DEFAULT nextval('public.cards_id_seq'::regclass);


--
-- Name: decks id; Type: DEFAULT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.decks ALTER COLUMN id SET DEFAULT nextval('public.decks_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: david
--

COPY public.alembic_version (version_num) FROM stdin;
252d27e0e43b
\.


--
-- Data for Name: cards; Type: TABLE DATA; Schema: public; Owner: david
--

COPY public.cards (id, name, type, colors, cmc) FROM stdin;
1	snapcaster mage	creature	blue	2
2	lightning bolt	instant	red	1
3	emrakul, the aeons torn	creature	colorless	15
4	grim flayer	creature	black-green	2
5	lashweed lurker	creature	colorless	8
6	glimmer of genius	instant	blue	4
7	botanical sanctum	land	colorless	0
10	Tarmogoyf	Creature	Green	2
17	Mana Confluence	Land	\N	\N
\.


--
-- Data for Name: decks; Type: TABLE DATA; Schema: public; Owner: david
--

COPY public.decks (id, title, format, colors, creator) FROM stdin;
1	jund	modern	black-red-green	reid duke
2	esper dragons	standard	white-blue-black	shota yasooka
\.


--
-- Name: cards_id_seq; Type: SEQUENCE SET; Schema: public; Owner: david
--

SELECT pg_catalog.setval('public.cards_id_seq', 17, true);


--
-- Name: decks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: david
--

SELECT pg_catalog.setval('public.decks_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: cards cards_pkey; Type: CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.cards
    ADD CONSTRAINT cards_pkey PRIMARY KEY (id);


--
-- Name: decks decks_pkey; Type: CONSTRAINT; Schema: public; Owner: david
--

ALTER TABLE ONLY public.decks
    ADD CONSTRAINT decks_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

