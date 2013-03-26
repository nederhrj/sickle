# coding: utf-8
"""
    record.py

    <FILLER>

    :copyright: Copyright 2013 - Rene Nederhand
"""

from lxml import etree

import re
from sickle.models import Record, Header

ns = {'mods': 'http://www.loc.gov/mods/v3',
      'xml': 'http://www.w3.org/XML/1998/namespace',
      'dai': 'info:eu-repo/dai',
      'gal': 'info:eu-repo/grantAgreement',
      'didl' : 'urn:mpeg:mpeg21:2002:02-DIDL-NS',
      'hbo' : 'info:eu-repo/xmlns/hboMODSextension'
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
            names = self.getNames()
            abstract = self.getAbstract()
            title = self.getTitle()
            subjects = self.getSubjects()
            department = self.getDepartment()
            print title
            print names
            print subjects
            print department

    def xpath(self, node, path):
        result = node.xpath(path, ns)
        return result and result[0] or ''

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
        # Author: //dc:creator
        # Advisor: //dc:contributor
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
        # Abstract: //dc:description[@label='abstract']
        return self.xml.xpath('.//mods:abstract/text()', namespaces=ns)

    def getTitle(self):
        # Title: //dc:title
        title = []
        mainTitle = self.xml.xpath('.//mods:titleInfo/mods:title/text()', namespaces=ns)
        subTitle = self.xml.xpath('.//mods:titleInfo/mods:subTitle/text()', namespaces=ns)
        title.append(mainTitle)
        title.append(subTitle)
        return title

    def getSubjects(self):
        # Keyword: //dc:subject[@label='keywords']
        return self.xml.xpath('.//mods:subject/mods:topic/text()', namespaces=ns)

    def getAffiliation(self):
        # Role: //dc:creator/@role
        return self.xml.xpath('.//mods:name/mods:affiliation/text()', namespaces=ns)

    def getLanguage(self):
        # Language: //dc:language
        return self.xml.xpath('.//mods:language/text()', namespaces=ns)

    def getDateIssued(self):
        # Date: //dc:date
        #TODO: Some date cleaning
        return self.xml.xpath('.//mods:originInfo/mods:dateIssued/text()', namespaces=ns)

    def getGenre(self):
        # Documenttype: //dc:type
        return self.xml.xpath(".//mods:genre/text()", namespaces=ns)

    def getFile(self):
        # File: //dc:identifier
        return self.xml.xpath(".//didl:Item/didl:Resource/@ref", namespaces=ns)

    def getDomain(self):
        # Domain: //dc:subject[@label='domain']
        return self.xml.xpath(".//mods:classification[@authority='nbc']/text()", namespaces=ns)

    def getInternshipCompany(self):
        # Intern-ship Company: //dc:description[@label='setting']
        return self.xml.xpath(".//mods:name[role='cli']/text()", namespaces=ns)

    def getIdentifier(self):
        # Identifier: //dc:identifier[@label='registration']
        return self.xml.xpath(".//identifier/text()", namespaces=ns)

    def getFormat(self):
        # Format: //dc:Format
        return self.xml.xpath(".//didl:Item/didl:Resource/@/text()", namespaces=ns)

    def getRights(self):
        # Rights: //dc:rights
        return self.xml.xpath(".//didl:Item/didl:Resource/@mimeType/text()", namespaces=ns)

    # Functions for HBO mods
    def getDepartment(self):
        # Institute: //dc:publisher[@label='department']
        return self.xml.xpath(".//hbo:namePart[@type='department']/text()", namespaces=ns)

    def getOrganisation(self):
        # Organisation: //dc:publisher[@label='organisation']
        # TODO: If not exist -> Add to list of organisations[]
        return self.xml.xpath(".//hbo:namePart[@type='organisation']/text()", namespaces=ns)

    def getLectorate(self):
        # Organisation: //dc:publisher[@label='organisation']
        # TODO: If not exist -> Add to list of organisations[]
        return self.xml.xpath(".//hbo:namePart[@type='lectorate']/text()", namespaces=ns)

    # Functions for publications
    def getJournal(self):
        return self.xml.xpath(".//mods:relatedItem[@type='host']/mods:titleInfo/text()", namespaces=ns)

    def getPublisher(self):
        return self.xml.xpath(".//mods:relatedItem[@type='host']/mods:originInfo/mods:publisher/text()", namespaces=ns)

    def getPlace(self):
        return self.xml.xpath(".//relatedItem[@type='host']/mods:originInfo/mods:place/text()", namespaces=ns)

    def getISBN(self):
        return self.xml.xpath(".//relatedItem[@type='host']/identifier[@type='uri']/text()", namespaces=ns)

    def getVolume(self):
        return self.xml.xpath(".//mods:relatedItem[@type='host']/mods:part/mods:detail[@type='volume']/text()", namespaces=ns)

    def getIssue(self):
        return self.xml.xpath(".//mods:relatedItem[@type='host']/part/detail[@type='issue']/text()", namespaces=ns)

    def getStartPage(self):
        return self.xml.xpath(".//mods:relatedItem[@type='host']/part/extend[@unit='page']/start", namespaces=ns)

    def getEndPage(self):
        return self.xml.xpath(".//mods:relatedItem[@type='host']/part/extend[@unit='page']/end", namespaces=ns)

    def getDAI(self):
        return self.xml.xpath(".//mods:extension/dai:daiList/dai:identifier[@authority='info:eu-repo/dai/nl']/text()", namespaces=ns)

















