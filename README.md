Bordone Room
============

Bordone Room is a free web application for self-hosted photo galleries. It uses
Django and some JavaScript libraries.

[![Build Status](https://travis-ci.com/bbliem/bordone-room.svg?branch=master)](https://travis-ci.com/bbliem/bordone-room)


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

## Operating behind a reverse proxy

If you run the app behind a reverse proxy, you may find that the URLs Django generates contain internal IP addresses instead of the original host. One way of fixing this is making your reverse proxy set the `X-Forwarded-Host` and `X-Forwarded-Proto` headers accordingly. Apache, for example, seems to set `X-Forwarded-Host` out-of-the-box, but for `X-Forwarded-Proto` it seems you need to add the following line to your Apache configuration:
```
RequestHeader set "X-Forwarded-Proto" expr=%{REQUEST_SCHEME}
```
Now, to make Django take these headers into account, set the environment variable `USE_PROXY_HEADERS` to `true` (e.g., in your `.env` file).

## Usage

For uploading photos, creating albums and editing content, a user account is
required. At the moment, users cannot register via the web. To create a user
account, use the `manage.py` script in the project root as follows:

```
manage.py createsuperuser
```

Photos can be uploaded using the web interface after logging in. When a photo
is uploaded, its visibility is initially set to private. That is, only
logged-in users can see it. To make photos publicly available, make sure you
are logged in, then click the edit button, select the respective photos and
click the *Public* checkbox. In the edit menu, photos can also be arranged into
albums or deleted.

A more low-level interface for changing content is provided by the *admin
interface*, which can be accessed in your browser using the path `/admin/`.

At the moment, the admin interface is the only way to add or edit albums, but
we will probably provide a user-friendly interface soon.


## License

Bordone Room is free software licensed under the GNU General Public License
(version 3). See the file `COPYING.md` for details.
