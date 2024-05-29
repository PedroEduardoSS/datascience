import scrapy
import re
import urllib.parse

from enum import Enum
class Tipo(Enum):
    PROJETO_DE_LEI = 1
    INDICACAO = 9
    EMENDAS_E_SUBSTITUTIVOS = 4005
    ANEXOS = 4001
    PROJETO_DE_LEI_COMPLEMENTAR = 2
    MOCAO = 6
    PARECER = 4000
    AUTOGRAFO = 18
    PROPOSTA_DE_EMENDA = 5
    REQUERIMENTO = 7
    PROPOSTA_DE_ALTERACAO = 108
    OFICIO = 19
    PROJETO_DE_DECRETO_LEGISLATIVO = 4
    REQUERIMENTO_DE_INFORMACAO = 8
    MENSAGEM_ADITIVA = 47
    VETO = 4002
    PROJETO_DE_RESOLUCAO = 3


class AlSpPlSpider(scrapy.Spider):
    name = "al_sp_pl"
    #allowed_domains = ["www.al.sp.gov.br"]
    qtd_rows = 20
    def start_requests(self):
        tipos = [1,9,4005,4001,2,6,4000,18,5,7,108,19,4,8,47,4002,3]
        for tipo in tipos:
            yield scrapy.Request(url=f"https://www.al.sp.gov.br/alesp/pesquisa-proposicoes/?direction=top&lastPage=0&currentPage=1&act=detalhe&idDocumento=&rowsPerPage={self.qtd_rows}&currentPageDetalhe=1&tpDocumento=&selecionaDeseleciona=nao&method=search&natureId={tipo}&text=&legislativeNumber=&legislativeYear=&natureIdMainDoc=&anoDeExercicio=&strInitialDate=&strFinalDate=&author=&supporter=&politicalPartyId=&stageId=", callback=self.parse)
    
    def parse(self, response):
        # tipo_proposicoes = {1,9,4005,4001,2,6,4000,18,5,7,108,19,4,8,47,4002,3}
        
        resultados = []
        for elem in response.xpath("//tbody/tr"):
            titulo_projeto_lei = elem.xpath(".//td[2]/a/strong/text()").extract_first()
            if not titulo_projeto_lei:
                # Linha nula, ignorar
                continue
            

            dados = {
                'proposição': elem.xpath(".//td[2]/a/strong/text()").extract_first().split(',')[0].strip(),
                'numero': titulo_projeto_lei.split(',')[0].split('/')[0].split(' ')[-1].strip(),
                'ano': titulo_projeto_lei.split(',')[1].split('/')[2][:4],
                'tipo': int(response.url.split("&")[10].split('=')[1]),#Tipo(int(response.url.split("&")[10].split('=')[1])).name,
                'ementa': elem.xpath("//a/following-sibling::br/following-sibling::text()").extract_first().strip(),
                'url': f"https://www.al.sp.gov.br{elem.xpath('.//td[2]/a/@href').extract_first()}"
            }
            
            resultados.append(dados)
            print(dados)
