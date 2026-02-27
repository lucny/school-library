Architektura projektu
=====================

Aplikace
--------

- ``core``: homepage, healthcheck, zakladni sablony.
- ``accounts``: registrace, login/logout, reset hesla, role, OAuth.
- ``catalog``: knihy, autori, kategorie, prilohy.
- ``circulation``: rezervace, vypujcky, vraceni, prodlouzeni.
- ``reviews``: hodnoceni (1-5), recenze, moderace.

Data a vazby
------------

- ``Book`` ma autory a kategorie (M2M).
- ``Reservation`` a ``Loan`` se vazou na ``Book`` a uzivatele.
- ``Rating`` a ``Review`` se vazou na ``Book`` a uzivatele.

Role
----

- ``reader``: bezny ctenar, muze hodnotit a rezervovat.
- ``librarian``: sprava provozu knihovny, moderace recenzi, vypujcky.

Technologie
-----------

- Django 5
- django-allauth (OAuth)
- SQLite (vyvoj), PostgreSQL (Docker/provoz)
- Django templates + lehky AJAX
