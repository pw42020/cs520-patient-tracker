<p align="center">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
<img src="https://github.com/pw42020/cs520-repo/actions/workflows/actions.yml/badge.svg">
<img src="./coverage.svg">
<img src="https://img.shields.io/badge/code%20style-black-000000.svg">
<img src="https://img.shields.io/badge/linting%20-pylint-FFD700.svg">
<img src="https://img.shields.io/badge/FLASK-005571?style=for-the-badge&logo=flask">
</p>

## Patient Tracker API
Created by Matthew Lips, Dhruv Maheshwari, Navid Tabrizi, Patrick Walsh

Documentation for the API can be found [here](https://pw42020.github.io/cs520-patient-tracker/).

### Installation and Usage
First, install the repository via

```sh
git clone https://github.com/pw42020/cs520-patient-tracker
```

Once the repository is installed, `cd` into the root of the repository through

```sh
cd cs520-patient-tracker
```

> Note: Ensure you have python's virtualenv library installed using `pip install virtualenv`

Inside of the repository, create a new virtual environment and activate it via

```sh
python -m virtualenv .venv
source .venv/bin/activate
```

Once this is complete, install all required dependencies by writing

```sh
pip install -r requirements.txt
```

Once all of the requirements are installed, the API should be good to use! To run, simply write:

```sh
cd src
flask run
```

and your output should be something like

```sh
cs520-patient-tracker/src on  feature/create-test-suite [$!?] via 🐍 3.9.6 via cs520-patient-tracker 
➜ flask run
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

To ensure the database is on and running, open a separate terminal and enter `curl http://127.0.0.1:5000`. If your output says, `Pinged your deployment. You successfully connected to MongoDB!`, your deployed API is good to go!

### Generate documentation
```sh
cd docs
make html
```

You should get output like this:
```sh
cs520-patient-tracker/docs on  main [$!?] via 🐍 3.9.6 via cs520-patient-tracker 
➜ make html
Running Sphinx v7.2.6
/Users/patrickwalsh/dev/cs520-patient-tracker/.venv/lib/python3.9/site-packages/urllib3/__init__.py:34: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
  warnings.warn(
loading pickled environment... done
building [mo]: targets for 0 po files that are out of date
writing output... 
building [html]: targets for 0 source files that are out of date
updating environment: 0 added, 1 changed, 0 removed
reading sources... [100%] index
looking for now-outdated files... none found
pickling environment... done
checking consistency... done
preparing documents... done
copying assets... copying static files... done
copying extra files... done
done
writing output... [100%] index
generating indices... genindex py-modindex done
writing additional pages... search done
dumping search index in English (code: en)... done
dumping object inventory... done
build succeeded.

The HTML pages are in _build/html.
```

and opening `_build/html/index.html` in Chrome should show all of the documentation!