# -*- coding: gbk -*-

from page_parser import PageParser, DocInfo
from template_parser import TemplateParser
from list_parser import ListParser
import config
import time

def gen_page_list():
    url = 'http://www.doutula.com/article/list/?page={page_num}'
    template_name = config.TEMPLATE_DIR + 'doutula.list.template'
    template_parser = TemplateParser(template_name)
    list_parser = ListParser(template_parser.xpath_list)
    for num in range(1, 132):
        page_url = url.format(page_num=num)
        # print 'page_url => ' + page_url
        info_dict = list_parser.parse(page_url)
        time.sleep(config.TIME_INTERVAL)
        for e in info_dict['list']:
            print e

def gen_docs():
    page_list = []
    with open(config.DATA_DIR + 'page_list.txt') as fin:
        for line in fin:
            page_list.append(line.rstrip())
    template_name = config.TEMPLATE_DIR + 'doutula.template'
    template_parser = TemplateParser(template_name)
    page_parser = PageParser(template_parser.xpath_list)
    for page_url in page_list[1104: ]:
        info_list = page_parser.parse(page_url)
        if len(info_list) > 0:
            for docinfo in info_list:
                print docinfo
        else:
            print 'page parse fail.'

def main():
    # gen_page_list()
    gen_docs()

if __name__ == '__main__':
    main()
