# Epiquote

Epiquote is a bash.org-like website to submit, display, vote for and comment
quotes (from IRC or real life).

## Installing a development environment

    git clone git@github.com:seirl/epiquote.git
    cd epiquote
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cp epiquote/settings/{conf.sample.py,dev.py}
    $EDITOR epiquote/settings/dev.py
    python3 manage.py migrate
    python3 manage.py runserver

## Contributing

Send (PEP8 compliant) pull-requests here:
https://github.com/seirl/epiquote/pulls
