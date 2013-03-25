# coding: utf-8
"""
    record.py

    <FILLER>

    :copyright: Copyright 2013 - Rene Nederhand
"""

from lxml import etree

import re
from sickle.models import Record, Header

MODS_NAMESPACE = '{http://www.loc.gov/mods/v3}'

ns = {'mods': 'http://www.loc.gov/mods/v3',
      'xml': 'http://www.w3.org/XML/1998/namespace',
      'dai': 'info:eu-repo/dai',
      'gal': 'info:eu-repo/grantAgreement',
      'didl' : 'urn:mpeg:mpeg21:2002:02-DIDL-NS'
      }


class ModsRecord2(Record):
    def __init__(self, record_element, strip_ns=True, nsMap={}):
        super(Record, self).__init__(record_element, strip_ns=strip_ns)
        self.nsMap=nsMap
        self.header = Header(self.xml.find(
            './/' + self._oai_namespace + 'header'))
        self.deleted = self.header.deleted
        if not self.deleted:
            self.metadata = self.xml.find('.//' + self._oai_namespace + 'metadata')
            #print "METADATA ",  self.metadata
            names = self.getNames()
            abstract = self.getAbstract()
            print names, abstract

    def _concatenateNames(self, family=None, given=None):
        """
        Concatenate family and given names to one String
        :param family:
        :param given:
        :return: String
        """
        name = ""
        if family:
            name += family
        if given:
            name += ', ' + given
        return name

    def _getNameParts(self, name):
        names = []
        for namePart in name.xpath('mods:namePart', namespaces=ns):
            type = namePart.xpath('@type', namespaces=ns)[0]
            if type == 'family':
                family = namePart.xpath('text()', namespaces=ns)[0]
            elif type == 'given':
                given = namePart.xpath('text()', namespaces=ns)[0]
        person = self._concatenateNames(family, given)
        names.append(person)
        return names

    def getNames(self):
        authors = []
        advisors = []
        organisations = []

        for name in self.xml.xpath('.//mods:name', namespaces=ns):
            role = name.xpath('mods:role/mods:roleTerm/text()',  namespaces=ns)[0]
            if role == 'aut':
                authors = self._getNameParts(name)
            elif role == 'ths':
                advisors = self._getNameParts(name)
            else:
                for namePart in name.xpath('mods:namePart', namespaces=ns):
                    print role, namePart.xpath('text()', namespaces=ns)[0]
                    organisations.append(namePart.xpath('text()', namespaces=ns)[0])
        return authors, advisors, organisations

    def getAbstract(self):
        return self.xml.xpath('.//mods:abstract/text()', namespaces={'mods': 'http://www.loc.gov/mods/v3'})










