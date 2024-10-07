class listas:
    
    def __init__(self) -> None:
        pass
    
    def __call__(self, name_list: str) -> list[str]:
        
        self.lista = getattr(self, name_list, None)
        list = None
        if self.lista:
            list = self.lista()
            
        return list
    

    def elaw_cadastro(self) -> list[str]:
        return [
            "AREA_DIREITO", "SUBAREA_DIREITO", "ESTADO", "COMARCA", "FORO",
            "VARA", "DATA_DISTRIBUICAO", "PARTE_CONTRARIA", "TIPO_PARTE_CONTRARIA", "DOC_PARTE_CONTRARIA",
            "EMPRESA", "TIPO_EMPRESA", "DOC_EMPRESA", "ADVOGADO_INTERNO",
            "ADV_PARTE_CONTRARIA", "ESCRITORIO_EXTERNO", "VALOR_CAUSA"
        ]
        
    def elaw_complement(self) -> list[str]:
        return [
            "UNIDADE_CONSUMIDORA", "DIVISAO", "ACAO", "DATA_CITACAO", 
            "DESC_OBJETO", "OBJETO", "PROVIMENTO", "FATO_GERADOR", "FASE"
        ]



    def caixa_emissao(self) -> list[str]:
        return ["AUTOR", "CPF_CNPJ_AUTOR", "REU", "CPF_CNPJ_REU", "TRIBUNAL", "COMARCA", "VARA", "AGENCIA",
                "TIPO_ACAO", "VALOR_CALCULADO", "TEXTO_DESC", "DATA_PGTO", "NOME_CUSTOM", "VIA_CONDENACAO"]


    def esaj_emissao(self) -> list[str]:
        return ["NOME_PARTE", "TIPO_GUIA", "FORO", "CLASSE", "VALOR_CAUSA", "NOME_INTERESSADO",
                "CPF_CNPJ", "TIPO_INTERESSADO", "PRAZO_PGTO"]


    def elaw_pagamentos(self) -> list[str]:
        return ["TIPO_GUIA", "VALOR_GUIA", "DATA_LANCAMENTO", "TIPO_PAGAMENTO", "SOLICITANTE", "TIPO_CONDENACAO",
                "COD_BARRAS", "DOC_GUIA", "DOC_CALCULO", "CNPJ_FAVORECIDO", "DESC_PAGAMENTO"]


    def elaw_download(self) -> list[str]:
        return ["TERMOS"]


    def elaw_provisao(self) -> list[str]:
        return ["PROVISAO", "DATA_ATUALIZACAO", "VALOR_ATUALIZACAO", "OBSERVACAO"]


    def elaw_andament(self) -> list[str]:
        return ["TIPO_ANDAMENTO", "DATA", "OCORRENCIA", "OBSERVACAO", "ANEXOS", "TIPO_ANEXOS"]


    def movimentacao(self) -> list[str]:
        return ['DATA_PUBLICACAO', "DATA_LIMITE", "PALAVRA_CHAVE", "INTIMADO", "TRAZER_DOC", "TRAZER_TEOR", "NOME_MOV"]


    def protocolo(self) -> list[str]:
        return ["TIPO_PROTOCOLO", "SUBTIPO_PROTOCOLO", "PARTE_PETICIONANTE", "TIPO_ARQUIVO", "PETICAO_PRINCIPAL", "ANEXOS", "TIPO_ANEXOS"]

    def tjdft_calculo(self) -> list[str]:
        
        return ["REQUERENTE", "REQUERIDO", 
                "JUROS_PARTIR", "DATA_INCIDENCIA", "JUROS_PERCENT",
                "VALOR_CALCULO", "DATA_CALCULO", 
                "MULTA_PERCENTUAL", "MULTA_DATA", 
                "MULTA_VALOR", "PERCENT_MULTA_475J", 
                "HONORARIO_SUCUMB_PERCENT", "HONORARIO_SUCUMB_DATA",
                "HONORARIO_SUCUMB_VALOR", "HONORARIO_SUCUMB_PARTIR",
                "HONORARIO_CUMPRIMENTO_PERCENT", "HONORARIO_CUMPRIMENTO_DATA", 
                "HONORARIO_CUMPRIMENTO_VALOR", "HONORARIO_CUMPRIMENTO_PARTIR",
                "CUSTAS_DATA", "CUSTAS_VALOR"]
