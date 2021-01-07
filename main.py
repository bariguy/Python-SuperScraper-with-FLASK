# from indeed import extract_pages, extract_indeed_jobs, extract_jobs_and_companies
# from save import save_to_file

# pages = extract_pages()
# indeed_jobs = extract_indeed_jobs(pages)
# save_to_file(indeed_jobs)


from flask import Flask, render_template, request, redirect
from scrapper import get_jobs
from export import save_to_file

app = Flask("SuperScrapper")

db = {}

@app.route("/")
def job():
    return render_template("template.html")

@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
        
    else: 
        return redirect("/")

    return render_template("report.html", searchingBy = word, resultsNumber = len(jobs), jobs = jobs)

@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()

        save_to_file(jobs) 
        return "DONE"
    except:
        return redirect("/")



app.run(debug=True)