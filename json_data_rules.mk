# JSON files are run through jsonproc, which is a tool that converts JSON data to an output file
# based on an Inja template. https://github.com/pantor/inja

AUTO_GEN_TARGETS += $(DATA_C_SUBDIR)/items.h

$(DATA_C_SUBDIR)/items.h: $(DATA_C_SUBDIR)/items.json $(DATA_C_SUBDIR)/items.json.txt
	$(JSONPROC) $^ $@

$(C_BUILDDIR)/item.o: c_dep += $(DATA_C_SUBDIR)/items.h

# Path to randomizer python script
PYTHON_SCRIPT = sensible_randomizer2.py

# Rule to *conditionally* generate wild_encounters.json using the Python script
ifeq (,$(shell test -f $(DATA_C_SUBDIR)/wild_encounters.json && echo exists))
$(DATA_C_SUBDIR)/wild_encounters.json: $(PYTHON_SCRIPT)
	@echo "Generating wild_encounters.json because it does not exist..."
	python3 $(PYTHON_SCRIPT) > $@
else
  $(DATA_C_SUBDIR)/wild_encounters.json:
	@echo "wild_encounters.json already exists, skipping generation."
endif

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
