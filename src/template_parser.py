# -*- coding: gbk -*-

class TemplateParser(object):
    def __init__(self, template_file):
        self.xpath_list = []
        with open(template_file) as fin:
            for line in fin:
                field_name, xpath, attr_key = line.rstrip().split(',')
                if len(attr_key) == 0:
                    attr_key = None
                self.xpath_list.append( (field_name, xpath, attr_key) )
