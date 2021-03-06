
from BaiduImg_Spider.demo1_raw import url_Searcher, decoder, downloader, searcher_threadpool, downloader_multiprocess_pool

__author__ = 'pwjworks'
__github__ = 'https://github.com/pwjworks/baiduImgSpider'

class ImgSpider(object):
    """
    下载百度图片原图的脚本
    基于urllib,selenium并进行多线程优化
    """
    def __init__(self):
        self.url_searcher_threads = []
        self.seacher = url_Searcher.Searcher()
        self.decoder = decoder.Decoder()
        self.downloader = downloader.Downloader()
        self.downloader_pool = []

    def create_threads_pool(self):
        """
        创建图片链接爬取器（url_searcher）的线程，并开始任务
        :return:
        """
        for i in range(2):
            self.url_searcher_threads.append(searcher_threadpool.Searcher_Threadpool(self.seacher))

    def wait_all_complete(self):
        """
        等待所有url_searcher线程完成任务
        :return:
        """
        for thread in self.url_searcher_threads:
            thread.join()
        self.seacher.driver.quit()

    def create_multiprocessing_pool(self):
        """
        创建图片下载器（url_searcher）的进程，并开始任务
        :return:
        """
        for i in range(3):
            self.downloader_pool.append(downloader_multiprocess_pool.Downloader_multiprocess_pool(self.downloader))

    def fill_index_queue(self):
        """
        把爬取到的url数目放入队列中，方便下载器下载
        :return:
        """
        for i in range(1, self.seacher.num):
            self.downloader.index_queue.put(i)

    def decode_url(self):
        """
        解码url并把url放入downloader的url队列中
        :return:
        """
        while not self.seacher.url_queue.empty():
            self.downloader.url_queue.put(decoder.Decoder.decode_url(self.decoder, self.seacher.url_queue.get()))


if __name__ == '__main__':
    spider = ImgSpider()
    spider.create_threads_pool()
    spider.wait_all_complete()
    spider.decode_url()
    spider.fill_index_queue()
    spider.create_multiprocessing_pool()
