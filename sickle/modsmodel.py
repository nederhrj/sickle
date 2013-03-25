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
            tag = element.tag
            if strip_ns:
                tag = re.sub(r'\{.*\}', '', tag)
            # We need to look for specific attributes
            # like <mods:namePart type="family">FamilyName</mods:namePart>
            # TODO: family and given name should be kept together
            if tag == 'name':
                # name//namePart
                tag_name = defaultdict(list)
                for item in element.getchildren():
                    if item.items() != []:

                        attribute = item.items()[0][0]
                        #print "ATTRIBUTE NAME: ", attribute
                        #print "CONTENTS", item.get(attribute)
                        #print "VALUE: ", item.text
                        #print "items : ", item.get('type'), item.text
                        tag_name[item.get(attribute)].append(item.text)
                    else:
                        if strip_ns:
                            tag = re.sub(r'\{.*\}', '', item.tag)
                            #print "ELEMENT : ", tag, item.text
                            tag_name[tag].append(item.text)
                    #print tag, item.get('type'), item.text, item.text
                    #iter('namePart'):
                    #print [{item.get('type'):item.text for item in element.getchildren()}]
                print tag_name




                names = element.getchildren()
                for name in names:
                    items = name.items()
                    #print items
                    for item in items:
                        pass
                #        print item
                #        print element.get(item[1])
                #print names
                #print element.get('type')
                #print element.text

                #print [{element.get('type'):element.text for name in names}]



            if tag == "namePart":
                element_type = element.get('type')
                if element_type:
                    # Create a new tag
                    newtag = tag + '-' + element_type
                    #print newtag + ' = ' + element.text
                    fields[newtag].append(element.text)
            print tag, element.text
            fields[tag].append(element.text)
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

            #print type(self.metadata), self.metadata.items() # dict


