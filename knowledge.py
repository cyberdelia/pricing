# -*- coding: utf-8 -*-
import datetime

# We are importing pyke knowledge engine
from pyke import knowledge_engine

# === Finding out which package apply for the duration ===

# Given existings packages and duration, prints which package apply 
# or if no package applies.
def which_package(packages, duration):
    # We are loading Pyke rules base we have defined in pricing.krb
    engine = knowledge_engine.engine((__file__, '.rules'))
    engine.activate('pricing')
    # We are creating the facts base from the package list.
    for package in packages:
        engine.assert_('packages', 'package', (package,))
        
    # Now, we have our rules and our facts, let's just prove that a package applies.
    try:
        vals, plans = engine.prove_1_goal('pricing.packages($type, $delta)', delta=duration)
        print vals['type']
    # We cannot prove that any package applies, so, no package applies.
    except knowledge_engine.CanNotProve:
        print "No package can apply"
    
    # We need to reset the engine to be able to apply a new fact base.
    engine.reset()


# === Let's try with a few examples ===

# Defining a bunch of duration
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

# This should print 'No package apply'
print "You should read 'No package can apply' :",
which_package(['weekly'], a_day)
