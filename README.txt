A database of "Thursday's Club" meeting attendence and gifts
------------------------------------------------------------

The scripts need access to the Django database and models, and so can't be run
standalone. Instead they are run via the django_extensions's 'runscript'
subcommand which invokes the 'run()' method inside the given script.

  python manage.py runscript plot_tenure
