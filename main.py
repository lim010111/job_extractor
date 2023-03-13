from extractors.ind import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs

what = input("what do you want to search for? : ")
where = input("where is the location that you search for? : ")

indeed = extract_indeed_jobs(what, where)
wwr = extract_wwr_jobs(what)

jobs = indeed + wwr

file = open(f"{what}.csv", "w")
file.write("Position, Company, location, URL\n")

for job in jobs:
    file.write(
        f"{job['position']}, {job['company']}, {job['location']}, {job['link']}\n"
    )

file.close()
