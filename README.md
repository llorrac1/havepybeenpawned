# Have Py Been Pawned?

## Overview: 
[HaveIBeenPawned](https://haveibeenpwned.com/) is a well-known website which aggregegates email breach data. It allows people to search their email address via the website and they also have an API.

This script and jupyter notebook allow you to run your own list of emails against the Have I Been Pawned API to find out if they appear in any breaches that HIBP have loaded. 

## What this repo contains
A jupyer notebook and an equivalent script

## Why did I build it?
1. It's handy to be able to find out whether a list of email addresses appear in any data breaches
2. HaveIBeenPawned doesn't support bulk email address lookup as of February 2021
3. It's easy to extend this and analyse the addresses further with pandas 
 
There are a couple of scripts floating around but I didn't like the way they were written, or they used superseded API or Python versions. 

Thought someone else might find this useful, so figured I'd share it.

## Whats it do?: 
This tool takes a csv of email addresses and hits the HaveIBeenPawned API to find out whether those email addresses appear in any breaches

## Requirements:
- Python 3.9 (probably works on 3xx but I haven't tested it)
- Some standard python libs
- An HIBP API Key https://haveibeenpwned.com/API/Key 
  - *(Don't forget to read the docs https://haveibeenpwned.com/API/v3#Authorisation)*
- A csv file containing email addresses in the first column 

## How to use it 

First, set up a virtual environment

```console
foo@bar:~$ python3 -m venv env
```

Then activate it
```console
foo@bar:~$ source env/bin/activate
```

### For the Jupyter Notebook
In the Second Cell: 

1. Update the `fileLocation` variable to the location of your email source file

2. Update the `apikey` and `user-agent` variables to your HIBP API Key and a relevant user-agent per HIBP docs https://haveibeenpwned.com/API/v3#Authorisation 

Run all cells

### For the Script 
In settings.py: 

1. Update the `fileLocation` variable to the location of your email source file
2. Update the `apikey` and `user-agent` variables to your HIBP API Key and a relevant user-agent per HIBP docs https://haveibeenpwned.com/API/v3#Authorisation 
3. Save changes 

And back in your terminal run
```console
foo@bar:~$ python3 hibp.py
```
