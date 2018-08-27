# poetweet

Django poetry app writes random arrangements of poetry to twitter.

Poetry is parsed using the management/commands from poet's works. I parse as well as possible into small fragments of less than 280 characters. Fragments are stored with stanza and line information in a sqllite database.

Currently tweets can be sent manually from a simple html page, in templates. This gives the option to refresh for a new randomly generated fragment, type a custom tweet, and send.

Not shown is the secret keys for authenticating the twitter APIs, as well as the rest of the Django framework, just the app.

# Todo

App needs to be placed on a server, like a raspberry pi, and django-celery implemented to automate tweet sending.

I would like to have an better way to upload poetry. Currently text files have to be placed manually, or lines can be entered in a APIview html page.

Analytics and a nice analytics viewer will be added.
