# Description

- Search for an item in the Babac catalog
- Returns the first 10 items

# Python requirements

- sopel
- bs4 (BeautifulSoup)
- cookielib
- mechanize
- yaml

*it currently only works with Python 2. cookielib and mechanize are specific to Python 2.*

# Instructions

## To configure the module

- Change the username and password in config.yml.example
- Rename config.yml.example to config.yml
- Specify the path to the config.yml file in load_config()

## Running the module

In a channel where the bot is present, enter the following command:

```
> .babac training wheels
```

The output should looks like that:

```
> Searching in the Babac catalog for: training+wheels
> Returning 3 items.
> #Babac | Item name and price
> 22-169 | Stabilizers & Trainers 16-24 | 20.00$
> 22-155 | Wald Stabilizer 16 – 26″ | 40.00$
> 22-150 | WALD Training Wheels | 35.00$
```

# Future features

- Nicier formatting of the output
- Everything running with Python3
  * Replace mechanize for another module
- Have links to product pages within the product numbers output
- If there are more than 10 items found, return how many items found and include instructions to get the list of all items found
