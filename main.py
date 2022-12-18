from flask import Flask, render_template, request, redirect, send_file
from so import search_jobs as search_so_jobs
from indeed import search_jobs as search_indeed_jobs
from export import save_to_file

app = Flask('JobScrapper')

db = {}

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result')
def result():
    keyword = request.args.get('keyword')
    if keyword:
        keyword = keyword.lower()
        fromDb = db.get(keyword)
        #print(fromDb)

        if fromDb is None:

            so_jobs = search_so_jobs(keyword)
            indeed_jobs = search_indeed_jobs(keyword)
            jobs = so_jobs + indeed_jobs

            db[keyword] = jobs

        else:
            jobs = fromDb

        return render_template(
            'result.html',
            searchingBy=keyword,
            resultNum=len(jobs),
            results=jobs
            )

    else:
        return redirect('/')


@app.route('/export')
def export():
    try:
        keyword = request.args.get('keyword')
        keyword = keyword.lower()
        if keyword is None:
            print("No keyword!")
            raise Exception()
        
        jobs = db.get(keyword)
        if jobs is None:
            print("No results!")
            raise Exception()

        save_to_file(jobs)

        return send_file(
            'jobs.csv',
            as_attachment=True,
            attachment_filename=f'{keyword}.csv'
            )

    except:
        return redirect('/')


app.run(host='0.0.0.0')
