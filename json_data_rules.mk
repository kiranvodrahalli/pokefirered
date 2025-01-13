# JSON files are run through jsonproc, which is a tool that converts JSON data to an output file
# based on an Inja template. https://github.com/pantor/inja

AUTO_GEN_TARGETS += $(DATA_C_SUBDIR)/items.h

$(DATA_C_SUBDIR)/items.h: $(DATA_C_SUBDIR)/items.json $(DATA_C_SUBDIR)/items.json.txt
	$(JSONPROC) $^ $@

$(C_BUILDDIR)/item.o: c_dep += $(DATA_C_SUBDIR)/items.h

# TODO(kiranv): Auto-generate wild_encounters.json by running the python randomizer first.
# Path to your Python script (adjust if necessary)
PYTHON_SCRIPT = sensible_randomizer2.py

# Rule to generate wild_encounters.json using the Python script
$(DATA_C_SUBDIR)/wild_encounters.json: $(PYTHON_SCRIPT)
	python3 $(PYTHON_SCRIPT) > $@

AUTO_GEN_TARGETS += $(DATA_C_SUBDIR)/wild_encounters.h
$(DATA_C_SUBDIR)/wild_encounters.h: $(DATA_C_SUBDIR)/wild_encounters.json $(DATA_C_SUBDIR)/wild_encounters.json.txt
	$(JSONPROC) $^ $@

$(C_BUILDDIR)/wild_encounter.o: c_dep += $(DATA_C_SUBDIR)/wild_encounters.h

AUTO_GEN_TARGETS += $(DATA_C_SUBDIR)/region_map/region_map_entry_strings.h
$(DATA_C_SUBDIR)/region_map/region_map_entry_strings.h: $(DATA_C_SUBDIR)/region_map/region_map_sections.json $(DATA_C_SUBDIR)/region_map/region_map_sections.strings.json.txt
	$(JSONPROC) $^ $@

$(C_BUILDDIR)/region_map.o: c_dep += $(DATA_C_SUBDIR)/region_map/region_map_entry_strings.h

AUTO_GEN_TARGETS += $(DATA_C_SUBDIR)/region_map/region_map_entries.h
$(DATA_C_SUBDIR)/region_map/region_map_entries.h: $(DATA_C_SUBDIR)/region_map/region_map_sections.json $(DATA_C_SUBDIR)/region_map/region_map_sections.entries.json.txt
	$(JSONPROC) $^ $@

$(C_BUILDDIR)/region_map.o: c_dep += $(DATA_C_SUBDIR)/region_map/region_map_entries.h
