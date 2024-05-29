import scrapy

from enum import Enum
class Tipo(Enum):
    ATO_DO_PRESIDENTE = 8
    DECRETO_LEGISLATIVO = 7
    DECRETO_MUNICIPAL = 9
    EMENDA_LEI_ORGANICA = 10
    LEI_COMPLEMENTAR = 3
    LEI_ORDINARIA = 6
    LEI_ORGANICA = 5
    PORTARIA = 1
    RESOLUCAO = 4

class CmUbPlSpider(scrapy.Spider):
    name = "cm_ub_pl"
    allowed_domains = ["e-processos.camarauberlandia.mg.gov.br"]
    '''
    start_urls = [
        #"https://e-processos.camarauberlandia.mg.gov.br/default_index_html",
        "https://e-processos.camarauberlandia.mg.gov.br/consultas/materia/materia_pesquisar_proc?txt_numero=&txt_ano=&txt_num_protocolo=&txt_num_processo=&dt_apres=&dt_apres2=&hdn_cod_autor=&txt_assunto=&lst_tramitou=&lst_localizacao=&lst_status=&rad_tramitando=&rd_ordenacao=1&incluir=&existe_ocorrencia=0&txt_relator=&lst_cod_partido=&lst_tip_autor=&hdn_txt_autor=&chk_coautor=&dt_public=&dt_public2="
    ]
    '''
    def start_requests(self):
        tipos = [8, 7, 9, 10, 3, 6, 5, 1, 4]
        qtd_rows = 50
        for tipo in tipos:
            yield scrapy.Request(url=f"https://e-processos.camarauberlandia.mg.gov.br/consultas/norma_juridica/norma_juridica_pesquisar_proc?lst_tip_norma={tipo}&step={qtd_rows}&txt_numero=&txt_ano=&dt_norma=&dt_norma2=&dt_public=&dt_public2=&lst_assunto_norma=&lst_tip_situacao_norma=&txt_assunto=&rd_ordenacao=1&incluir=", callback=self.parse)

    def parse(self, response):
        resultados = []
        for elem in response.xpath("//ul[@class='list-group list-group-flush']/li[@class='list-group-item']"):
            titulo_elemento = elem.xpath(".//span[@class='h6 font-weight-bold text-uppercase']/text()").get()
            dados = {
                'proposicao': titulo_elemento.split(',')[0],
                'numero': titulo_elemento.split(',')[0].split(' ')[-1],
                'ano': titulo_elemento.split(',')[1].split('/')[2],
                'tipo': int(response.url.split("&")[0].split('=')[1]),#Tipo(int(response.url.split("&")[0].split('=')[1])).name,
                'ementa': elem.xpath(".//div[2]/div/text()").extract_first().strip(),
                'url': elem.xpath(".//a/@href").extract_first()
            }
            resultados.append(dados)
            print(dados, end="\n\n")