--
-- PostgreSQL database dump
--

-- Dumped from database version 10.16 (Ubuntu 10.16-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 12.2

-- Started on 2021-04-05 12:05:43

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

--
-- TOC entry 2910 (class 0 OID 225875)
-- Dependencies: 198
-- Data for Name: block; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.block (id, name, video_url, ordering, views) FROM stdin;
1	Block 1	https://youtu.be/AZpu_U1HghE	1	0
2	Block 2	https://youtu.be/_VS5OfqSV4Q	2	0
3	Block 3	https://youtu.be/brwXb79JXEU	3	0
4	Block 4	https://youtu.be/AfdsJKWygao	4	0
5	Block 5	https://youtu.be/tHJIS7iMBZ8	5	0
6	Block 6	https://youtu.be/wULUT2joJvc	6	0
7	Block 7	https://youtu.be/PMH0aFHdaxE	7	0
8	Block 8	https://youtu.be/9qmALHRoVL4	8	0
9	Block 9	https://youtu.be/75Mw8r5gW8E	9	0
10	Block 10	https://youtu.be/RGXcRBomfuc	10	0
\.


--
-- TOC entry 2913 (class 0 OID 225890)
-- Dependencies: 201
-- Data for Name: page; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.page (id, name, slug, ordering) FROM stdin;
2	Page 1	page-1	2
3	Page 2	page-2	3
4	Page 3	page-3	4
5	Page 4	page-4	5
6	Page 5	page-5	6
\.


--
-- TOC entry 2915 (class 0 OID 225904)
-- Dependencies: 203
-- Data for Name: page_block_through; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.page_block_through (id, page_id, block_id) FROM stdin;
1	2	1
2	2	3
3	2	10
4	3	1
5	3	3
6	4	3
7	4	8
8	4	7
9	5	1
10	5	4
11	6	2
12	6	9
13	6	6
\.


--
-- TOC entry 2924 (class 0 OID 0)
-- Dependencies: 197
-- Name: block_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.block_id_seq', 10, true);


--
-- TOC entry 2925 (class 0 OID 0)
-- Dependencies: 196
-- Name: block_ordering_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.block_ordering_seq', 10, true);


--
-- TOC entry 2926 (class 0 OID 0)
-- Dependencies: 202
-- Name: page_block_through_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.page_block_through_id_seq', 13, true);


--
-- TOC entry 2927 (class 0 OID 0)
-- Dependencies: 200
-- Name: page_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.page_id_seq', 6, true);


--
-- TOC entry 2928 (class 0 OID 0)
-- Dependencies: 199
-- Name: page_ordering_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.page_ordering_seq', 6, true);


-- Completed on 2021-04-05 12:05:45

--
-- PostgreSQL database dump complete
--

