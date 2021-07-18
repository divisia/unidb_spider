from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Spider
from scrapy_splash import SplashRequest


class StudyInTurkeyCrawler(CrawlSpider):
    name = 'studyinturkey'
    allowed_domains = ['studyinturkey.gov.tr']
    start_urls = ['https://studyinturkey.gov.tr/StudyInTurkey/SiteMap']
    rules = (Rule(LinkExtractor(), callback="parse_item", process_request="add_cookies"),)


    def parse_item(self, response):
        try:
            try: phone = response.css('.adres-satir::text')[2].get()
            except: phone = None
            try: address = response.css('.adres-satir::text')[1].get()
            except: address = None
            data = {
                "name": response.css('strong::text').get(),
                "url": response.css('a.okul-web::attr(href)').get(),
                "phone": phone,
                "address": address,
                "logo": response.css('.okul-logo img::attr(src)').get(),
                "mail": response.css('html body.scrool-kayma div.arama-genel.kunye-genel div.container div.row.justify-content-end div.col-12.col-lg-4.col-md-5.arama-mobil.kunye-tablo div.kunye-tablo-ic div.okul-logo.kunye-satir.erasable div.adres-satir a::attr(href)').get(),

                "theses": response.css('html body.scrool-kayma div.tab-content div#dvUniversityProfile.tab-pane.fade.in.active.show div.container-fluid.okul-imkanlari.mt-5 div.row div.col-lg-2.col-md-4.col-sm-6.imkan-tablo div.renk4 span::text').get(),
                "sport_teams": response.css('html body.scrool-kayma div.tab-content div#dvUniversityProfile.tab-pane.fade.in.active.show div.container-fluid.okul-imkanlari.mt-5 div.row div.col-lg-2.col-md-4.col-sm-6.imkan-tablo div.renk1 span::text').get(),
                "communities": response.css('html body.scrool-kayma div.tab-content div#dvUniversityProfile.tab-pane.fade.in.active.show div.container-fluid.okul-imkanlari.mt-5 div.row div.col-lg-2.col-md-4.col-sm-6.imkan-tablo div.renk2 span::text').get(),
                "dorm_capacity": response.css('html body.scrool-kayma div.tab-content div#dvUniversityProfile.tab-pane.fade.in.active.show div.container-fluid.okul-imkanlari.mt-5 div.row div.col-lg-2.col-md-4.col-sm-6.imkan-tablo div.renk3 span::text').get(),
                "labs": response.css('html body.scrool-kayma div.tab-content div#dvUniversityProfile.tab-pane.fade.in.active.show div.container-fluid.okul-imkanlari.mt-5 div.row div.col-lg-2.col-md-4.col-sm-6.imkan-tablo div.renk5 span::text').get(),
                "area": response.css('html body.scrool-kayma div.tab-content div#dvUniversityProfile.tab-pane.fade.in.active.show div.container-fluid.okul-imkanlari.mt-5 div.row div.col-lg-2.col-md-4.col-sm-6.imkan-tablo div.renk6 span::text').get(),

                "assc_students": response.css("#onlisansOgrenciSayi::text").get(),
                "licn_students": response.css("#lisansOgrenciSayi::text").get(),
                "mast_students": response.css("#yuksekLisansOgrenciSayi::text").get(),
                "phd_students": response.css("#doktoraOgrenciSayi::text").get(),
                
                "staff_total": response.css("html body.scrool-kayma div.tab-content div#dvUniversityProfile.tab-pane.fade.in.active.show div.container-fluid.insan-kaynaklari div.container div#counter.row div.col-lg-5.academik-genel.text-center.wow.bounceInUp.delay-1s span::text").get(),
                "instructor": response.css("#ogretimGorevlisi::text").get(),
                "assc_prof": response.css("#docent::text").get(),
                "resc_asst": response.css("#arastirmaGorevlisi::text").get(),
                "prof": response.css("#profesor::text").get(),
                "foreign_staff": response.css("html body.scrool-kayma div.tab-content div#dvUniversityProfile.tab-pane.fade.in.active.show div.container-fluid.insan-kaynaklari div.container div#counter.row div.col-lg-7.academik-diger div.row div.col-sm-4.mb-2.wow.fadeInRight.delay-3s span::text").get(),
                "doctor_fmember": response.css("#doctorLecturer::text").get(),

                "assc_prog": response.css("html body.scrool-kayma div.tab-content div#dvUniversityProfile.tab-pane.fade.in.active.show div.container-fluid.programlar div.container div.row div.col-lg-3.col-md-6.col-sm-6.wow.fadeInLeft.delay-1s span::text").get(),
                "licn_prog": response.css("html body.scrool-kayma div.tab-content div#dvUniversityProfile.tab-pane.fade.in.active.show div.container-fluid.programlar div.container div.row div.col-lg-3.col-md-6.col-sm-6.wow.fadeInLeft.delay-2s span::text").get(),
                "mast_prog": response.css("html body.scrool-kayma div.tab-content div#dvUniversityProfile.tab-pane.fade.in.active.show div.container-fluid.programlar div.container div.row div.col-lg-3.col-md-6.col-sm-6.wow.fadeInRight.delay-3s span::text").get(),
                "phd_prog": response.css("html body.scrool-kayma div.tab-content div#dvUniversityProfile.tab-pane.fade.in.active.show div.container-fluid.programlar div.container div.row div.col-lg-3.col-md-6.col-sm-6.wow.fadeInRight.delay-4s span::text").get(),
            }
            print("##################################", data)
            yield data

        except Exception as e: print("ERR ######### ERR ############ ERR", e, response.css('strong::text').get(), response)
    
    def add_cookies(self, request, *args, **kwargs):
        request.cookies['TS0156c298'] = '01026844b87fc22903c2e380333fd1cd4410cfbf818b721cc4bb27e662302a6903ebc908c18241a52dc7a46ae0c6be8a7345a428d0552ef2c394a2cd573203186267469d918d2264cf587134472538a540f16914c6'
        request.cookies['BIGipServerpool_studyinTurkeyYOK'] = '1442910380.20480.0000'
        request.cookies['ASP.NET_SessionId'] = 'gzhr50sjltkxzqoy1hgxu1r5'
        return request
