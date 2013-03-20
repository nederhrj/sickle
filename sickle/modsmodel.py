# coding: utf-8
"""
    ModsModel

    Extends Record class for MODS support (http://www.loc.gov/standards/mods/mods.xsd)

    :copyright: Copyright 2013 - Rene Nederhand
"""

from sickle.models import Set, Record, Header, MetadataFormat, Identify
from .utils import get_namespace, xml_to_dict
from lxml import etree
import re
from collections import defaultdict

def xml_to_dict(tree, paths=['.//'], nsmap={}, strip_ns=False):
    """Convert an XML tree to a dictionary.

    :param paths: An optional list of XPath expressions applied on the XML tree.
    :param nsmap: An optional prefix-namespace mapping for conciser spec of paths.
    :param strip_ns: Flag for whether to remove the namespaces from the tags.
    """
    fields = defaultdict(list)
    for path in paths:
        elements = tree.findall(path, nsmap)
        for element in elements:
            #attributes = element.keys()
            #for attribute in attributes:
            tag = element.tag
            #    attr = element.get(attribute)
            if strip_ns:
                tag = re.sub(r'\{.*\}', '', tag)
            if tag == "namePart":
                element_type = element.get('type')
                if element_type:
                    newtag = tag + '-' + element_type
                    print "namePart GEVONDEN", element.items()
                    #print element.get('type')
                    #fields[tag + 'family'].append(element.get('family'))
                    #fields[tag + 'given'].append(element.get('given'))
                    print newtag + ' = ' + element.text
                    fields[newtag].append(element.text)
            fields[tag].append(element.text)

             #   fields[attribute].append(attr)
    return dict(fields)



class ModsRecord(Record):
    """Represents an MODS record
    :param record_element: The XML element 'record'.
    :param strip_ns: Flag for whether to remove the namespaces from the element names.
    """
    #super(Record).__init__()
    def __init__(self, record_element, strip_ns=True):
        super(Record, self).__init__(record_element, strip_ns=strip_ns)
        self.header = Header(self.xml.find(
                    './/' + self._oai_namespace + 'header'))
        self.deleted = self.header.deleted
        if not self.deleted:
            mtd = self.xml.find('.//' + self._oai_namespace + 'metadata')


            self.metadata = xml_to_dict(
                self.xml.find('.//' + self._oai_namespace + 'metadata'
                ).getchildren()[0], strip_ns=self._strip_ns)

            print type(self.metadata), self.metadata.items() # dict



