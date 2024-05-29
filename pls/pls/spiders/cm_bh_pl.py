import scrapy


class CmBhPlSpider(scrapy.Spider):
    name = "cm_bh_pl"
    allowed_domains = ["www.cmbh.mg.gov.br"]
    '''
    start_urls = [
        "https://www.cmbh.mg.gov.br/atividade-legislativa/pesquisar-proposicoes",
        f"https://www.cmbh.mg.gov.br/atividade-legislativa/pesquisar-proposicoes/{tipo_nome}/{numero}/{ano}"
    ]
    '''
    def start_requests(self):
        tipos = [
            "autorizacao",
            "indicacao",
            "mocao",
            "oficio",
            "prestacao-de-contas",
            "projeto-de-decreto-legislativo",
            "projeto-de-lei",
            "projeto-de-resolucao",
            "proposta-de-emenda-a-lei-organica",
            "recurso",
            "representacao",
            "requerimento",
            "requerimento-de-comissao",
            "sugestao-de-proposicao",
        ]
        #for tipo_nome in tipos:
        tipo_nome = "projeto-de-lei"
        numero = 906
        ano = 2024
        yield scrapy.Request(url="https://www.cmbh.mg.gov.br/atividade-legislativa/pesquisar-proposicoes", callback=self.parse)

    def parse(self, response):
        resultados = []
        for elem in response.xpath("//ul[@id='resultadoPesquisaInterno']/li"):
            #titulo_elemento = elem.xpath(".//span[@class='h6 font-weight-bold text-uppercase']/text()").get()

            dados = {
                'proposicao': elem.xpath(".//h3/span[1]").extract_first(),
                'numero': "",#elem.xpath("//*[@id='proposicoes-interna']/h2/span/text()").extract_first().split(' ')[-1].split('/')[0],
                'ano': "",#elem.xpath("//*[@id='proposicoes-interna']/h2/span/text()").extract_first().split(' ')[-1].split('/')[0],
                'tipo': "",
                'ementa': elem.xpath(".//*[@id='proposicoes-interna']/div/p[2]/text()").extract_first().strip(),
                'url': f"https://www.cmbh.mg.gov.br/atividade-legislativa/pesquisar-proposicoes/{tipo_nome}/{numero}/{ano}"
            }
            resultados.append(dados)

            print(dados, end="\n\n")
