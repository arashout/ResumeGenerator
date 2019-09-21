generate: resumes/resume.fs.yaml main.py ResumeGenerator.py
	pipenv run python main.py resumes/resume.fs.yaml -o arash_outadi_resume.pdf 
trim: 
	pdfseparate -f 1 arash_outadi_resume.pdf %d.pdf
	rm 2.pdf
	mv 1.pdf arash_outadi_resume.pdf