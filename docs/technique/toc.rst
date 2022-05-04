.. _toc:

table of content - toc
======================

Tyes
----

Dotted
~~~~~~

They are two types of dotted tocs. One with and one without dots between
the section title and the section page.

Level
~~~~~

Strategies
----------

Regex
~~~~~

See :class:`reftable.toc.strategy.regex`.

Geometry
~~~~~~~~

Looking for a Box which is wider than higher. What a ratio do we need?

Look for matching pairs of text and a number on the right side.

Geometry plus Regex
~~~~~~~~~~~~~~~~~~~

Combine Geometry and Regex approach.

See :class:`groupme.toc.strategy.georegex`.

Example
-------

.. code-block :: none

    1. Einleitung ................................................................ 1
        1.1 Fragestellung und Zielsetzung .........................................2
        1.2 Aufbau der Arbeit .................................................... 3

    2. Das Social Web und die Privatsphäre  –
       Selbstdarstellungsverhalten der Nutzer aus Sicht von Massenmedien und Literatur ....  4
       2.1 Web 2.0, Social Web und Social Media: Abgrenzungen und Definitionen.............. 4
       2.2 Merkmale von Social Network Sites................................................ 8
       2.3 Eigenschaften netzbasierter Kommunikation ........................................10
       2.4 Einführung in das Konzept der Privatheit .........................................11
       2.5 Darstellungen in Massenmedien und Literatur  .................................... 12
         2.5.1 Selbstdarstellung und Privatheit als Problemfelder .......................... 12
         2.5.2 Mögliche Gründe für die Freizügigkeit im Umgang mit privaten Daten .......... 16
         2.5.3 Privacy Paradox und Post-Privacy ............................................ 18
