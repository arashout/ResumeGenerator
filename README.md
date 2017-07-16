# ResumeGenerator
Generate a PDF resume formatted as perscribed by [Gayle McDowell from CareerCup, author of Cracking The Coding Interview](https://www.careercup.com/resume)
using your [JSON resume](https://jsonresume.org/schema/).
Here's a ![preview of what it will look like](preview_resume.pdf)
## Instructions

### Setup resume.json

Before running the command line program there are a couple changes to the json resume we need to make:
1. Inside **location** objects, everywhere there is **region** key we need to add a **regionCode** key
e.g `"region": "British Columbia", "regionCode": "BC"`
2. Inside all education items add a `location` object with `regionCode` keys as well
3. Add a new category `"projects"` formatted similar to the volunteer category
Notice the new fields `websiteName` and `githubRepo`
e.g
```javascript
"projects": [
    {
        "name": "Strength Journal",
        "website": "https://play.google.com/store/apps/details?id=site.arashout.workoutnotebook",
        "websiteName": "Google Play Store",
        "githubRepo": "https://github.com/arashout/StrengthJournal",
        "summary": "An Android workout tracker that let’s you jump straight into recording your exercises",
        "technologies": [
            "Kotlin",
            "Java",
            "XML",
            "SQLite"
        ]
    },
    {
        "name": "Blob Combat Simulation",
        "website": "",
        "websiteName": "",
        "githubRepo": "https://github.com/arashout/BlobCombatSimulator",
        "summary": "Developed a simulation where 'blobs' evolve to fight using neural networks and different genetic selection algorithms",
        "technologies": [
            "C++",
            "SFML",
            "QtCreator",
            "Eigen"
        ]
    }
]
```
A full example [resume.json](resume.json)

### Clone Repo and Install Requirements
The next step is to clone the repository and install the requirements
```bash
git clone https://github.com/arashout/ResumeGenerator.git
cd ResumeGenerator
pip3 install -r requirements.txt
```
Also note you have to install [wkhtmltopdf](https://github.com/pdfkit/pdfkit/wiki/Installing-WKHTMLTOPDF)

### Generate PDF resume from command-line
You can generate your pdf resume by running (inside the cloned repo)
```bash
python generateResume.py path_to_resume.json
```
Optionally you can anonymize your PDF by supplying a second argument
```bash
python generateResume.py path_to_resume.json -a path_to_anon_data.json
```
Where `anon_data.json` is a json dictionary where the keys are sensitive information
you want to replace and the values are generic text to replace them with
e.g.
```javascript
{
    "CA" : "UN",
    "California" : "Unknown Province",
    "John Doe" : "First Last",
    "myname" : "firstlast",
    "Software Resume" : "Anon Resume",
    "Workout Logger" : "Android App",
    "The Times" : "School Newspaper"
}
```
