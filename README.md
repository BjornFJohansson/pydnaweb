# webpcr

is a flask app that contains a PCR simulator and a Tm calculator.
It is built on top of [pydna](https://github.com/BjornFJohansson/pydna).

[![webpcr](static/webpcr.png)](http://bjornfjohansson.pythonanywhere.com/#)

It is available online [here](http://bjornfjohansson.pythonanywhere.com/#).

or here: https://bit.ly/pydnawebpcr

[a blogpost](https://ochsavidare.blogspot.com/2013/12/webpcr-pcr-product-simulation.html)

Installed on [pythonanywhere](https://www.pythonanywhere.com) like this:

	mkvirtualenv --python=/usr/bin/python3.9 my-virtualenv
	pip install flask flask-wtf wtforms pydna
	git clone https://github.com/BjornFJohansson/webpcr.git


Session on PythonAnywhere

	14:44 ~ $ mkvirtualenv --python=/usr/bin/python3.9 my-virtualenv
	created virtual environment CPython3.9.5.final.0-64 in 15701ms
	  creator CPython3Posix(dest=/home/pydna/.virtualenvs/my-virtualenv, clear=False, no_vcs_ignore=False, global=False)
	  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/pydna/.local/share/virtualen
	v)
		added seed packages: pip==21.1.2, setuptools==57.0.0, wheel==0.36.2
	  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator
	virtualenvwrapper.user_scripts creating /home/pydna/.virtualenvs/my-virtualenv/bin/predeactivate
	virtualenvwrapper.user_scripts creating /home/pydna/.virtualenvs/my-virtualenv/bin/postdeactivate
	virtualenvwrapper.user_scripts creating /home/pydna/.virtualenvs/my-virtualenv/bin/preactivate
	virtualenvwrapper.user_scripts creating /home/pydna/.virtualenvs/my-virtualenv/bin/postactivate
	virtualenvwrapper.user_scripts creating /home/pydna/.virtualenvs/my-virtualenv/bin/get_env_details
	(my-virtualenv) 14:45 ~ $ pip install flask flask-wtf wtforms pydna
	Looking in links: /usr/share/pip-wheels
	Collecting flask
	  Downloading Flask-2.0.2-py3-none-any.whl (95 kB)
		 |████████████████████████████████| 95 kB 854 kB/s
	Collecting flask-wtf
	  Downloading Flask_WTF-0.15.1-py2.py3-none-any.whl (13 kB)
	Collecting wtforms
	  Downloading WTForms-2.3.3-py2.py3-none-any.whl (169 kB)
		 |████████████████████████████████| 169 kB 18.5 MB/s
	Collecting pydna
	  Downloading pydna-4.0.2-py3-none-any.whl (110 kB)
		 |████████████████████████████████| 110 kB 16.3 MB/s
	Collecting click>=7.1.2
	  Downloading click-8.0.3-py3-none-any.whl (97 kB)
		 |████████████████████████████████| 97 kB 1.4 MB/s
	Collecting itsdangerous>=2.0
	  Downloading itsdangerous-2.0.1-py3-none-any.whl (18 kB)
	Collecting Werkzeug>=2.0
	  Downloading Werkzeug-2.0.2-py3-none-any.whl (288 kB)
	  Downloading networkx-2.6.3-py3-none-any.whl (1.9 MB)
		 |████████████████████████████████| 288 kB 17.3 MB/s
	Collecting Jinja2>=3.0
	  Downloading Jinja2-3.0.2-py3-none-any.whl (133 kB)
		 |████████████████████████████████| 133 kB 7.9 MB/s
	Collecting MarkupSafe>=2.0
	  Downloading MarkupSafe-2.0.1-cp39-cp39-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_12_x86_64.manylinux2010_x86_64.whl (30 kB)
	Collecting pyparsing
	  Downloading pyparsing-2.4.7-py2.py3-none-any.whl (67 kB)
		 |████████████████████████████████| 67 kB 1.3 MB/s
	Collecting requests
	  Downloading requests-2.26.0-py2.py3-none-any.whl (62 kB)
		 |████████████████████████████████| 62 kB 88 kB/s
	Collecting networkx
	  Downloading networkx-2.6.3-py3-none-any.whl (1.9 MB)
		 |████████████████████████████████| 1.9 MB 3.8 MB/s
	Collecting biopython
	  Downloading biopython-1.79-cp39-cp39-manylinux_2_5_x86_64.manylinux1_x86_64.whl (2.3 MB)
		 |████████████████████████████████| 2.3 MB 10.6 MB/s
	Collecting prettytable
	  Downloading prettytable-2.2.1-py3-none-any.whl (23 kB)
	Collecting appdirs
	  Downloading appdirs-1.4.4-py2.py3-none-any.whl (9.6 kB)
	Collecting numpy
	  Downloading numpy-1.21.2-cp39-cp39-manylinux_2_12_x86_64.manylinux2010_x86_64.whl (15.8 MB)
		 |████████████████████████████████| 15.8 MB 16.9 MB/s
	Collecting wcwidth
	  Downloading wcwidth-0.2.5-py2.py3-none-any.whl (30 kB)
	Collecting charset-normalizer~=2.0.0
	  Downloading charset_normalizer-2.0.7-py3-none-any.whl (38 kB)
	Collecting urllib3<1.27,>=1.21.1
	  Downloading urllib3-1.26.7-py2.py3-none-any.whl (138 kB)
		 |████████████████████████████████| 138 kB 11.3 MB/s
	Collecting certifi>=2017.4.17
	  Downloading certifi-2021.10.8-py2.py3-none-any.whl (149 kB)
		 |████████████████████████████████| 149 kB 19.4 MB/s
	Collecting idna<4,>=2.5
	  Downloading idna-3.2-py3-none-any.whl (59 kB)
		 |████████████████████████████████| 59 kB 1.8 MB/s
	Installing collected packages: MarkupSafe, Werkzeug, wcwidth, urllib3, numpy, Jinja2, itsdangerous, idna, click, charset-normalizer, certifi, wtforms, requests, pyparsing, prettytable, networkx, flask, biopython, appdirs, pydna, flask-wtf
	Successfully installed Jinja2-3.0.2 MarkupSafe-2.0.1 Werkzeug-2.0.2 appdirs-1.4.4 biopython-1.79 certifi-2021.10.8 charset-normalizer-2.0.7 click-8.0.3 flask-2.0.2 flask-wtf-0.15.1 idna-3.2 itsdangerous-2.0.1 networkx-2.6.3 numpy-1.21.2 prettytable-2.2.1 pydna-4.0.2 pyparsing-2.4.7 requests-2.26.0 urllib3-1.26.7 wcwidth-0.2.5 wtforms-2.3.3
	(my-virtualenv) 14:48 ~ $


![settings](static/settings.png)


![wsgi](static/bjornfjohansson_pythonanywhere_com_wsgi_py.png)