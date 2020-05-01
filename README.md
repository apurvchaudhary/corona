# Corona Live Statistics
<h4>
Corona live counts display & statistics on country, state & district level of India.
</h4>
<ul>
<li>
Live counts of Corona confirmed patients, recovered, death & active.
</li>
<li>
Data is fetching from covid19.org APIs on periodic basis.
</li>
<li>
Live Data analysis through pie-chart, bar-graph, line-graph for better understanding of cases across the country.
</li>
<li>
Delta is also shown for daily cases of confirmed, recovered etc.
</li>
<li>
District search option is developed to search district by name or give 1st three letters so it will suggest the district name having those three letters.
</li>
<li>
This is open source project and you are welcome to contribute.
</li>
<li>
project url : http://ec2-3-135-201-128.us-east-2.compute.amazonaws.com/corona/home/
</li>
<li>
currently running on AWS ec2 with apache2 server
</li>
<li>
Tech Stack : python, django, djangorestframework, celery, celeery-beat, html, css, JS, Jquery
</li>
</ul>
<h4>
Installation setup : steps
</h4>
<ol>
<li>
git pull https:// this repository as it is public. 
</li>
<li>
create python3 virtual environment. (python >= 3.6.5 bcoz i have used f"str" formatting) :
~ python3 -m venv env_name
</li>
<li>
activate env : ~ source env_name/bin/activate
</li>
<li>
install requirements : ~ pip install -r path_to_requirement.txt
</li>
<li>
migrations : ~ python manage.py migrate
</li>
<li>
create superuser : ~ python manage.py createsuperuser
</li>
<li>
collect static files : ~ python manage.py collectstatic articulate_static
</li>
<li>
all these setup has dependency on settings.py, contact for settings.
</li>
<li>
finally run server : ~ python manage.py runserver
</li>
<li>
For periodic task run redis-server on port 6379 i.e default for broker then run celery worker and scheduler
</li>
<li>
celery command : ~ celery -A corona worker --beat --scheduler django --loglevel=info
</li>
<li>
else you can run beat & worker separately.
</li>
</ol>