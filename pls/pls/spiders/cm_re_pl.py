import scrapy

from enum import Enum
class Tipo(Enum):
    DECRETO = 5
    DECRETO_LEGISLATIVO = 4
    LEI = 1
    LEI_COMPLEMENTAR = 2
    RESOLUCAO = 3

class CmRePlSpider(scrapy.Spider):
    name = "cm_re_pl"
    allowed_domains = ["publico.recife.pe.leg.br"]
    #start_urls = ["https://publico.recife.pe.leg.br/default_index_html"]

    def start_requests(self):
        tipos = [5, 4, 1, 2, 3]
        qtd_rows = 50
        for tipo in tipos:
            yield scrapy.Request(url=f"https://publico.recife.pe.leg.br/consultas/norma_juridica/norma_juridica_pesquisar_proc?lst_tip_norma={tipo}&step={qtd_rows}&txt_numero=&txt_ano=&dt_norma=&dt_norma2=&dt_public=&dt_public2=&lst_assunto_norma=&lst_tip_situacao_norma=&txt_assunto=&rd_ordenacao=1&incluir=", callback=self.parse)

    def parse(self, response):
        resultados = []
        for elem in response.xpath("//ul[@class='list-group list-group-flush']/li[@class='list-group-item']"):
            titulo_elemento = elem.xpath(".//span[@class='h6 font-weight-bold text-uppercase']/text()").get()
            dados = {
                'proposicao': titulo_elemento.split(',')[0],
                'numero': titulo_elemento.split(',')[0].split(' ')[-1],
                'ano': titulo_elemento.split(',')[1].split('/')[2],
                'tipo': int(response.url.split("&")[0].split('=')[1]), #Tipo(int(response.url.split("&")[0].split('=')[1])).name,
                'ementa': elem.xpath(".//div[2]/div/text()").extract_first().strip(),
                'url': elem.xpath(".//a/@href").extract_first()
            }
            resultados.append(dados)
            print(dados, end="\n\n")
