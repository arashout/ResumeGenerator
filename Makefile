SRC  := resumes/resume.yaml
OUT  := arash_outadi_resume
SITE := ../arashout.site

# Build arash_outadi_resume.{html,pdf} from the YAML source.
generate: $(SRC) main.py ResumeGenerator.py
	uv run python main.py $(SRC) -o $(OUT)

# Publish to the portfolio site: the resume data (drives the HTML page) and the
# built PDF (served at /pdf/ash_outadi_resume.pdf).
publish: generate
	cp $(SRC) $(SITE)/_data/resume.yaml
	cp $(OUT).pdf $(SITE)/pdf/ash_outadi_resume.pdf

.PHONY: generate publish
