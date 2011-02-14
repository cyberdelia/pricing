# -*- coding: utf-8 -*-
import datetime

# Importing Pyke knowledge engine
from pyke import knowledge_engine

# === Finding out which package apply for the duration ===

# Given existings packages and duration, prints which package applies
# or if no package applies.
def which_package(packages, duration):
    # We are loading Pyke rules base we have defined in pricing.krb
    engine = knowledge_engine.engine((__file__, '.rules'))
    engine.activate('pricing')
    # Creating the facts base from the package list.
    for package in packages:
        engine.assert_('packages', 'package', (package,))
        
    # Now, we have our rules and our facts, let's just prove that a package applies.
    try:
        vals, plans = engine.prove_1_goal('pricing.packages($type, $delta)', delta=duration)
        print vals['type']
    # We cannot prove that any package applies therefore no package applies.
    except knowledge_engine.CanNotProve:
        print "No package applies"
    
    # Resetting the engine is needed to be able to apply a new fact base.
    engine.reset()


# === Let's try with a few examples ===

# Defining a bunch of durations
a_day = datetime.timedelta(days=1)
a_week = datetime.timedelta(days=7)
less_than_a_week = datetime.timedelta(days=4)
more_than_a_week = datetime.timedelta(days=9)

# This should print 'daily'
print "You should read 'daily' :",
which_package(['daily', 'weekly'], a_day)

# This should print 'weekly'
print "You should read 'weekly' :",
which_package(['daily', 'weekly'], a_week)

# This should print 'daily'
print "You should read 'daily' :",
which_package(['daily', 'weekly'], less_than_a_week)

# This should print 'weekly'
print "You should read 'weekly' :",
which_package(['daily', 'weekly'], more_than_a_week)

# This should print 'daily'
print "You should read 'daily' :",
which_package(['daily'], more_than_a_week)

# This should print 'No package applies'
print "You should read 'No package applies' :",
which_package(['weekly'], a_day)
