# coding: utf-8
"""
    test_mods

    test MODS support

    :copyright: Copyright 2013 - Rene Nederhand
"""

from sickle import Sickle

from sickle.modsmodel import ModsRecord


#sickle = Sickle('http://www.surfsharekit.nl:8080/oai/hhs/')
#sickle = Sickle("http://www.surfsharekit.nl:8080/oai/hh/")
sickle = Sickle('http://www.hbo-kennisbank.nl/oai')

# Map to MODS Record implementation
sickle.class_mapping['ListRecords'] = ModsRecord

records = sickle.ListRecords(metadataPrefix='didl', ignore_deleted=True)

records.next()
records.next()
records.next()