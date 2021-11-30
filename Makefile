generate: resumes/resume.platf.yaml main.py ResumeGenerator.py
	pipenv run python main.py resumes/resume.fs.yaml -o output/arash_outadi_resume
trim: 
	pdfseparate -f 1 arash_outadi_resume.pdf %d.pdf
	rm 2.pdf
	mv 1.pdf arash_outadi_resume.pdf
copy_to_portfolio resumes/resume.platf.yaml main.py ResumeGenerator.py:
	python3 main.py resumes/resume.platf.yaml -o output/platform.pdf
	cp resumes/resume.platf.yaml ../arashout.site/_data/resume.yaml 
	cp output/platform.pdf.pdf ../arashout.site/pdf/arash_resume.pdf