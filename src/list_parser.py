# -*- coding: gbk -*-

import requests
from lxml import etree
import config
from datetime import datetime

class ListParser(object):
    def __init__(self, xpath_list):
        self.xpath_list = xpath_list

    def parse(self, page_url):
        self.page_url = page_url
        list_dict = {}
        try:
            res = requests.get(self.page_url, headers=config.HEADERS, timeout=config.TIMEOUT)
            page = etree.HTML(res.content.decode(res.encoding))
            for field_name, path, attr_key in self.xpath_list:
                try:
                    elems = page.xpath(path)
                    # print field_name, path, attr_key
                    # print len(elems)
                    if attr_key is not None:
                        list_dict[field_name] = [elem.attrib[attr_key] for elem in elems]
                    else:
                        list_dict[field_name] = elems[0].text
                except Exception, e:
                    raise Exception(field_name + ',' + path + ' parse error, ' + str(e))
        except Exception, e:
            print e
        return list_dict
