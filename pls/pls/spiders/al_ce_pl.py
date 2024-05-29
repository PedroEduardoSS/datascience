import scrapy

from enum import Enum
class Tipo(Enum):
    projeto_lei = 1
    projeto_indi = 2
    projeto_decre = 3
    projeto_compl = 4
    projeto_emen = 5
    projeto_reso = 6
    projeto_mens = 7

class AlCePlSpider(scrapy.Spider):
    name = "al_ce_pl"
    allowed_domains = ["www2.al.ce.gov.br"]
    #start_urls = ["https://www2.al.ce.gov.br/legislativo/proposicoes/"]
    opcao = 'D' # ou 'T'
    tipo_num = 1
    def start_requests(self):
        tipos = [1, 2, 3, 4, 5, 6, 7]
        for tipo in tipos:
            if tipo == 1:
                self.tipo_num = tipo
                for page in range(1, 5):
                    yield scrapy.Request(url=f"https://www2.al.ce.gov.br/legislativo/proposicoes/numero.php?nome=27_legislatura&tabela={Tipo(self.tipo_num).name}&opcao={self.opcao}&absolutepage={page}", callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            resultados = []
            for elem in response.xpath("//body/center"):
                #titulo_elemento = elem.xpath(".//span[@class='h6 font-weight-bold text-uppercase']/text()").get()
                ano = elem.xpath(".//tr/td[1]/font[2]/text()").extract_first().split('/')[1].strip()
                dados = {
                    'proposicao': f"{response.xpath("//table[@id='AutoNumber2']//b/text()[1]").extract_first()}, n° {elem.xpath(".//tr/td[1]/font[2]/text()").extract_first()}",
                    'numero': elem.xpath(".//tr/td[1]/font[2]/text()").extract_first().split('/')[0],
                    'ano': f"200{ano}" if len(ano) == 1 else f"20{ano}",
                    'tipo': self.tipo_num,#response.xpath("//table[@id='AutoNumber2']//b/text()[1]").extract_first(),
                    'ementa': elem.xpath(".//a//text()").extract_first().strip(),
                    'url': f"https://www2.al.ce.gov.br{elem.xpath(".//a/@href").extract_first()}"
                }
                resultados.append(dados)
                print(dados, end="\n\n")
        else:
            print("Todos os dados foram processados")