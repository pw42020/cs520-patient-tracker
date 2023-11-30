## Patient Tracker API
Created by Matthew Lips, Dhruv Maheshwari, Navid Tabrizi, Patrick Walsh

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