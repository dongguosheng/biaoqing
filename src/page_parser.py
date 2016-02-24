# -*- coding: gbk -*-

import requests
from lxml import etree
import config
from datetime import datetime

class PageParser(object):
    def __init__(self, xpath_list):
        self.xpath_list = xpath_list

    def parse(self, page_url):
        self.page_url = page_url
        info_dict = {}
        try:
            res = requests.get(self.page_url, headers=config.HEADERS, timeout=config.TIMEOUT)
            info_dict['page_url'] = self.page_url
            page = etree.HTML(res.content.decode(res.encoding))
            for field_name, path, attr_key in self.xpath_list:
                try:
                    elems = page.xpath(path)
                    # print field_name, path, attr_key
                    # print len(elems)
                    if attr_key is not None:
                        info_dict[field_name] = [elem.attrib[attr_key] for elem in elems]
                    else:
                        info_dict[field_name] = elems[0].text
                except Exception, e:
                    raise Exception(field_name + ',' + path + ' parse error, ' + str(e))
            info_dict['last_modify'] = str(datetime.now())
        except Exception, e:
            print e
        assert(len(info_dict['pic_url']) == len(info_dict['desc']))
        info_list = [DocInfo(pic_url, info_dict['page_url'], desc, info_dict['title'], info_dict['last_modify']) for pic_url, desc in zip(info_dict['pic_url'], info_dict['desc'])]
        return info_list

class DocInfo(object):
    def __init__(self, pic_url, page_url, desc, title, last_modify):
        self.pic_url = pic_url
        self.page_url = page_url
        self.desc = desc
        self.title = title
        self.last_modify = last_modify
        self.desc_seg_list = []
        self.title_seg_list = []

    def __str__(self):
        return self.desc.encode('gbk', 'ignore') + '\n' + self.title.encode('gbk', 'ignore') + '\n' + self.pic_url + '\n' + self.page_url + '\n' + self.last_modify

    def __hash__(self):
        return hash(self.pic_url)

    def __eq__(self, other):
        return self.pic_url == other.pic_url
