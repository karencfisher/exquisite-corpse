Locale Translations
===================

This directory contains translation files for the GUI:

* .po files: per-language translations
* base.pot: template for creating a new po translation

Localizations are built using GNU gettext: https://www.gnu.org/software/gettext

Reference: https://simpleit.rocks/python/how-to-translate-a-python-project-with-gettext-the-easy-way/

Following text adapted from the [Pure Data project](https://github.com/pure-data/pure-data/blob/master/po/README.txt).

Quick Start
-----------

Install GNU gettext for your platform:

* macOS: via Homebrew: `brew install gettext`
* Linux: using your package manager, ie. for Debian: `sudo apt-get install gettext`
* Windows: not tested

Generate binary message catalog .mo files:

    make

Overview
--------

GUI strings are written in English and denoted in Python using the "\_()" function:

    _("Fold")

gettext searches the .py files for these marked strings and uses them as
unique identifiers to create the .pot template file which is simply a list of
string ids and translation stubs with associated metadata:

    msgid "Fold"
    msgstr ""

To create a new translation, add the appropriate ISO 639 2 or 3 letter language
code (ie. Spanish is "es_ES") to the `LOCALES` variable in the Makefile:

```Makefile
# en_US is default, support these additional locales
LOCALES = de_DE es_ES
```

Next, run make in this dir

    cd locale
    make

which will copy the base.pot template into a new base.po file in the following
subdirectory:
~~~
es_ES/LC_MESSAGES/base.po
~~~

_Note that some languages also have specific country distinctions, ie. Brazilian
Portuguese and Portuguese are named "pt_BR" & "pt_PT", respectively._

Next, fill out the msgstr portion for each msgid with it's translation:

    msgid "Fold"
    msgstr "Doble"

The translation process can either be done by hand with a text editor or via GUI
tools created for this purpose such as poedit: https://poedit.net. Any strings
left blank "" will use the default English string.

Generate binary message catalog .mo files:

    make

Now running the program should load any application translations using the
current locale. For example, if the locale of the system is German, gettext
should load the de locale. If the locale does not have a translation, the
default English text is used.

You can manually set the locale when running the program from the commandline
with the LANG or LC_MESSAGES environment variables, in this case German (de):

    LANG=de_DE ./exquisite

To see the current locale info:

    %locale
    LANG="en_US.UTF-8"
    ...

Developer Info
--------------

If any of the source files have changed, running `make` will update the template
and the po files.

To see the location of translation strings in the Python source files, run the
following in this directory:

    make locations
