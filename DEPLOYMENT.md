# Deploy Django on PythonAnywhere

The Netlify 404 occurs because this repository is a Django application. Netlify
publishes files but cannot run its Python WSGI server. The Django application
must first run on PythonAnywhere. These steps require access to your
PythonAnywhere account; no PythonAnywhere deployment has been performed yet.

## Set up the application

1. In a PythonAnywhere Bash console, clone this repository into
   `/home/YOUR_USERNAME/moviesstore`. Replace `YOUR_USERNAME` throughout these
   instructions with your PythonAnywhere username.
2. Create a fresh virtual environment with Python 3.12 or newer. Do not reuse
   the repository's `venv` directory, which contains environment-specific files:

   ```sh
   cd ~/moviesstore
   python3.12 -m venv ~/.virtualenvs/moviesstore
   source ~/.virtualenvs/moviesstore/bin/activate
   pip install -r requirements.txt
   ```

3. On PythonAnywhere's **Web** tab, add a web app using **Manual configuration**
   and the same Python version. Set its source directory to
   `/home/YOUR_USERNAME/moviesstore` and virtualenv directory to
   `/home/YOUR_USERNAME/.virtualenvs/moviesstore`.
4. Configure `DJANGO_SECRET_KEY` privately in the WSGI process environment with
   a new random secret of at least 50 characters. Never commit that value.
   Configure `DJANGO_ALLOWED_HOSTS` with your exact hostname, for example
   `YOUR_USERNAME.pythonanywhere.com` (no scheme or path). Ensure these variables
   are available to management commands as well. PythonAnywhere's WSGI process
   does not automatically inherit variables exported in a separate Bash console;
   load your private environment configuration before creating the application.
5. Replace the Web tab's WSGI file contents with the following, after loading
   the private environment configuration described above:

   ```python
   import os
   import sys

   sys.path.insert(0, '/home/YOUR_USERNAME/moviesstore')
   os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesstore.production_settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

## Verify settings and static files

With the virtualenv active and the private environment configured, run:

```sh
python manage.py check --settings=moviesstore.production_settings
python manage.py collectstatic --noinput --settings=moviesstore.production_settings
```

On the Web tab, map `/static/` to
`/home/YOUR_USERNAME/moviesstore/staticfiles`. Enable PythonAnywhere's HTTPS
redirect option, then reload the web app. Production cookies require HTTPS.

Database and uploaded-file storage configuration were not changed by this
deployment preparation. Confirm access to the existing data and movie images
before considering the deployment complete. The homepage and About page can
help verify that WSGI and static files work; movie, login, review, and order
flows also require working database tables. Inspect the Web tab's error log if
requests return a server error.

## Connect the public site

First confirm that `https://YOUR_USERNAME.pythonanywhere.com/` works, including
CSS, movie images, login, and the cart. You can use that address directly.

The working backend is `https://avaneeshm.pythonanywhere.com/`. Netlify now
publishes the `public` directory, whose `_redirects` file sends every path to
the corresponding PythonAnywhere path with a temporary HTTP 302 redirect.
For example, `/movies/` opens
`https://avaneeshm.pythonanywhere.com/movies/`. The browser uses the
PythonAnywhere address for the application, including login and cart requests,
so Django's host checks, cookies, and CSRF protection use the backend origin.

This routing takes effect after the Netlify deployment containing these files
is published. PythonAnywhere continues running Django and its existing SQLite
and Pillow setup; Netlify does not execute Python or host the database.
