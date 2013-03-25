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

class ModsRecord2(Record):
    def __init__(self, record_element, strip_ns=True, nsMap={}):
        super(Record, self).__init__(record_element, strip_ns=strip_ns)
        self.nsMap=nsMap
        self.header = Header(self.xml.find(
            './/' + self._oai_namespace + 'header'))
        self.deleted = self.header.deleted
        if not self.deleted:
            self.metadata = self.xml.find('.//' + self._oai_namespace + 'metadata')
            print "METADATA ",  self.metadata

            abstract = self.metadata.findall('.//' + MODS_NAMESPACE + 'abstract')

            editors = ""
            family = ""
            given = ""
            for name in self.nodeset(self.metadata, '//mods:mods/mods:relatedItem/mods:name'):
                if self.xpath(name, 'mods:role/mods:roleTerm/text()') == 'edt':
                    for namePart in self.nodeset(name, 'mods:namePart'):
                        type = self.xpath(namePart, '@type')
                        if type == 'family':  family = self.xpath(namePart, 'text()')
                        elif type == 'given':  given = self.xpath(namePart, 'text()')

            #keywords = self.metadata.findall('.//' + MODS_NAMESPACE + 'namePart/')

            #date = self.xml.xpath(self.metadata, '//mods:originInfo/mods:dateIssued/text()')

            #print [{element.tag: element.text for element in elements}]

    def xpath(self, node, path):
        result = node.xpath(path, self.nsMap)
        return result and result[0] or ''

    def nodeset(self, node, path):
            return node.xpath(path, self.nsMap)

    def _getMods(self, recordId):
        return


    def _getAbstract(self):
        return self.xml.xpath('.//' + MODS_NAMESPACE + 'mods:abstract', namespaces=self._oai_namespace)








