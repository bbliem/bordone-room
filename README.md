Bordone Room
============

Bordone Room is a free web application for self-hosted photo galleries. It uses
Django and some JavaScript libraries.


## Installation

Python 3.6 or later is required. The necessary dependencies are listed in the
file `requirements.txt`. The program `exiftool` must be installed on the
system.

For one of the Python dependencies, `PyExifTool`, a slightly modified version
is required that is not in PyPI. It can be installed by running the following
command:

```
pip install git+https://github.com/bbliem/pyexiftool.git
```

After this, the other dependencies can be installed with the following command:

```
pip install -r requirements.txt
```

## Configuration

The application can be configured by creating a file called `.env` in the project root directory.
An example configuration:

```
SECRET_KEY=<some secret random key>
ALLOWED_HOSTS=my.first.domain, my.second.domain
DEBUG=False
STATIC_ROOT=/var/www/bordone-static
MEDIA_ROOT=/var/www/bordone-media
DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=
EXIFTOOL=/usr/bin/vendor_perl/exiftool
```

Make sure that your web server allows access to `STATIC_ROOT` under the path
`/static/` but does not allow access to `MEDIA_ROOT` because only logged-in
users with the right permissions may be allowed to see some photos. The web
server user must have permissions to read and write to `MEDIA_ROOT`.

Depending on your setup, it may be necessary to edit some settings in
`bordone/settings.py`.

Instructions for deploying the application can be found in the [Django
documentation](https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/).


## License

Bordone Room is free software licensed under the GNU General Public License
(version 3). See the file `COPYING.md` for details.
