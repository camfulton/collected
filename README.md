## Installation:

- Set up a postgres DB and configure `DATABASE` settings in collected/settings.py
- `make install` to set up local deps (creates a virtualenv for you).
- `source .collected/bin/activate` to activate the virtualenv.
- `make migrate` to apply migrations to your database. 
- `make loaddb` to load up all the cards (will take a while, sorry).
- `make start` to run a local server.

## Use:
- You have to sign up and I put approximately 0 effort into making that a nice experience.
- http://127.0.0.1:8000/account/register/
- The activation link prints to the terminal--paste it into your browser.
- http://127.0.0.1:8000/account/login/
- Click the `collections` link and then `Create New Global Cards Collection` (I think this is the only one that actually works).
- Marvel at the totally unstyled Django form.
- "Name" can be anything -- it'll be the name of the collection in the list view.
- The check boxes indicate if you care about collecting foils &or nonfoils.
- The border drop down is in case you'd only like to collect a certain border.
- The gigantic unsorted list in the tiny box is every card in the database, best to click in and type what you are looking for. The perfect UX.
- Two good cards to take a look at are `Hymn to Tourach` and `Giant Spider` in Nonfoil and Foil.
- I should note it is totally possible to create a collection that has no cards in it if you select a border that has no printings, I don't think it gives any warning about this so if the resulting collection looks blank that is almost certainly why. 

## Where I have tested this and found it working:
- Python 3.8.5 running on Ubuntu 20.04.2 on WSL2 in Windows
- Postgres 12.6

## What is this project?

It's a prototype for a website to track a specific type of Magic: the Gathering collection.

Magic is a trading card game with some ~50,000 unique cards. In Magic, a card can have multiple printings in multiple languages over time.

A dedicated niche of collectors will sometimes choose their favorite card and try to collect a "global set" of that card - one copy of each printing in each language for a specific card or subset of cards.

The idea for the project was to see if the MTGJSON project had high enough quality data that I would feel comfortable maintaining a tool which would generate comprehensive global collection lists for any card you wanted to collect, as these can be very large and full of little-known sets  that often aren't included in the existing major card search tools.

Unfortunately, the data isn't quite up to snuff--particularly when it comes to language, which is one of the two most critical datapoints for global collecting. I don't have the time to devote to maintaining a list of this stuff, so until some other nerds on the internet do it I've abandoned this project.

That said, I got the project to the point where it will generate lists of most printings and their languages and will present them to you in a sort of ugly HTML table before deciding to drop it. There's no way to mark cards as collected or to exclude them from the generated list, but I believe there is support for it in the template and the databse.


## Which files are interesting?:

The bulk of the code exists on the models:

- collection/models.py
- mtg/models.py

This script loads the database from a JSON file provided by https://mtgjson.com/
It does some sanitization and reorganizing of the data to make it fit my purpose here
a bit better.

- mtg/management/commands/loaddb.py

## Why on earth are there no tests you dunce???:

- I am loathe to submit a code sample w/ no tests but I hadn't tested this
when I wrote it as it was just a prototype and I simply don't have the time to devote
to testing it now before shippping it your way. Apologies! Please know that I've been
woken up by pagerduty/spent enough time on bug duty in my life to value testing the code
I write for things that aren't toy weekend projects.