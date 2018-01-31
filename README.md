# forum-bot
A bot for logging in to a forum, scraping posts and summarising them.

Written in Python 3.6.3

## Background
When users post in forums and the information needs to be aggregated (e.g. competition entries), normally the forum admins end up having to keep track of new posts. This results in additional overhead as well as introducing mistakes. Users can become frustrated when their entries are missed and it may prevent future participation.

An alternative approach is to use a robot to scrape the subforum or thread and aggregate the posts automatically, provided users follow an agreed posting style. This is what this script hopes to achieve.

## Process
In order to edit posts to store the aggregated information, the bot needs to be able to log in to the site. This requires that future requests are authenticated and cookies are managed. The [Python package splinter](http://splinter.readthedocs.io/en/latest/why.html) achieves all of this using the [Firefox selenium driver](http://www.seleniumhq.org/download/).

When running commands a Firefox browser opens on your machine and this can be used to track the progress, which is really helpful for debugging.

## Backlog
Still to-do:
1. Allow threads with more than one page to be scraped (currently only first page is scraped).
2. Keep a database of threads/posts so that the main post is only edited when a new thread/post is added.
3. When keeping a database monitor old threads for edits.
4. Have the program parameterised so that classes, actions, etc can be passed in to the function.
5. Alow the program to read from a database so that multiple threads/posts can be monitored in one execution cycle.
