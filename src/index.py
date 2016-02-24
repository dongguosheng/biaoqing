# -*- coding: gbk -*-

from page_parser import DocInfo
import jieba
from operator import itemgetter
import config

class DocInfoIter(object):
    def __init__(self, filename, sep='|'):
        self.filename = filename
        self.sep = sep

    def __iter__(self):
        with open(self.filename) as fin:
            for line in fin:
                desc, title, pic_url, page_url, last_modify = line.rstrip().split(self.sep)
                yield DocInfo(pic_url, page_url, desc, title, last_modify)

class QueryInfo(object):
    def __init__(self, query_unicode):
        self.query_unicode = query_unicode
        self.query_seg_list = []

    def __str__(self):
        return query_unicode.encode('gbk', 'ignore')

class Index(object):
    def __init__(self):
        self.index_dict = {}
        self.docinfo_list = []

    def index(self, docinfo_iter):
        for docinfo in docinfo_iter:
            self.docinfo_list.append(docinfo)
            idx = len(self.docinfo_list) - 1
            docinfo.desc_seg_list = [w for w in jieba.cut(docinfo.desc, cut_all=False)]
            docinfo.title_seg_list = [w for w in jieba.cut(docinfo.title, cut_all=False)]
            for w in docinfo.desc_seg_list:
                self.index_dict.setdefault(w, set())
                self.index_dict[w].add(idx)
            for w in docinfo.title_seg_list:
                self.index_dict.setdefault(w, set())
                self.index_dict[w].add(idx)

    def query(self, query_unicode, topk=30):
        query_seg_list = jieba.cut(query_unicode, cut_all=False)
        query_info = QueryInfo(query_unicode)
        rs_set = set()
        for w in query_seg_list:
            query_info.query_seg_list.append(w)
            if w in self.index_dict:
                # union
                # rs_set |= self.index_dict[w]
                # intersection
                if len(rs_set) == 0:
                    rs_set |= self.index_dict[w]
                else:
                    rs_set &= self.index_dict[w]
        rs_list = self.rank(rs_set, query_info)
        return rs_list[: topk]

    def rank(self, rs_set, query_info):
        rs_list = []
        for idx in rs_set:
            score = self.__cal_rank(query_info, self.docinfo_list[idx])
            rs_list.append( (self.docinfo_list[idx], score) )
        return sorted(rs_list, key=itemgetter(1), reverse=True)

    def __cal_rank(self, query_info, docinfo):
        # TODO: add bm25
        return 1.0

def main():
    filename = config.DATA_DIR + 'docs'
    docinfo_iter = DocInfoIter(filename)
    index = Index()
    index.index(docinfo_iter)
    query_unicode = u'萌萌哒'
    rs_list = index.query(query_unicode)
    for docinfo, score in rs_list:
        print docinfo.desc, docinfo.pic_url, score

if __name__ == '__main__':
    main()
