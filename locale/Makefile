# build locale translations using gnu gettext
# refs:
# * https://simpleit.rocks/python/how-to-translate-a-python-project-with-gettext-the-easy-way/
# * https://phrase.com/blog/posts/translate-python-gnu-gettext/
# * https://github.com/pure-data/pure-data/tree/master/po

XGETTEXT = xgettext
MSGMERGE = msgmerge
MSGFMT = msgfmt

# .py files to check for translation strings, ie. _("string to translate")
FILES = $(wildcard ../*.py)

# en is default, support these additional locales
LOCALES = de

# translation source files, edit these
POFILES = $(addsuffix /LC_MESSAGES/base.po, $(LOCALES))

# translation message catalogs, generate these from po
MOFILES =  $(addsuffix /LC_MESSAGES/base.mo, $(LOCALES))

# translation template, create new locale po files from this
TEMPLATE = base.pot

all: template po mo

.PHONY: template locations

# refresh template.pot from the source code
template: $(TEMPLATE)

# base template in default en locale
$(TEMPLATE): $(FILES)
	touch $@
	$(XGETTEXT) --from-code=UTF-8 --no-location --sort-by-file \
		--package-name="Exquisite-corpse" \
		-d base -o $@ $^
	sed -i '' 's/charset=CHARSET/charset=UTF-8/g' $@

# print the locations for translation strings in the .py source files
locations:
	$(XGETTEXT) --from-code=UTF-8 --omit-header --output=- $(FILES)

# refresh .po files from the template
po: $(POFILES)

# the .po files depend on template.pot, suppress line location changes to
# avoid unnecessary updates
$(POFILES): %.po: $(TEMPLATE)
	mkdir -p $(dir $@)
	test -f $@ || cp $< $@
	$(MSGMERGE) --no-location --quiet --update $@ $(TEMPLATE)
	touch $@
	rm -f $@~

# generate .mo files from the .po files,
# these are installed and loaded by the GUI at runtime
mo: $(MOFILES)

# each .mo file depends on updates to the corresponding .po file
$(MOFILES): %.mo: %.po
	$(MSGFMT) -o $@ $(dir $@)base.po

# clean generated msg catalogs
clean:
	rm -f $(MOFILES)
