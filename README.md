# Script de Edição de Faixas MKV

Este script Python permite editar as faixas de arquivos MKV, alterando os títulos das faixas com base nas informações de idioma fornecidas. Ele utiliza as ferramentas `mkvmerge` e `mkvpropedit` para realizar as alterações nos arquivos MKV.


https://github.com/Nakasone-nsa/TrackRename/assets/137841760/8509a9c4-4f78-4e88-baa4-e31d2ff3d093


## Requisitos

- Python 3.x
- `mkvmerge` e `mkvpropedit` devem estar instalados no sistema e acessíveis pelo caminho (PATH)

## Instalação

1. Faça o download deste repositório em seu sistema.
2. Certifique-se de que o Python 3.x esteja instalado em sua máquina.
3. Certifique-se de que as ferramentas `mkvmerge` e `mkvpropedit` estejam instaladas e acessíveis pelo caminho (PATH) do sistema.

O script irá percorrer recursivamente o diretório especificado e localizar todos os arquivos MKV. Em seguida, ele criará arquivos JSON usando o `mkvmerge` para extrair informações sobre as faixas de áudio e legenda dos arquivos MKV. As informações extraídas serão salvas na pasta "temp" dentro do diretório do script.

Após a criação dos arquivos JSON, o script utilizará as informações para editar as faixas nos arquivos MKV. Os títulos das faixas serão alterados com base nas informações de idioma. Se uma faixa for marcada como "forced" (forçada), o título da faixa será alterado para "Forced". As alterações serão feitas usando a ferramenta `mkvpropedit`.

O progresso e os resultados das edições serão exibidos no console.

## Estrutura do Projeto

- `TrackRename.py`: O script principal que executa as ações de edição.
- `temp/`: Pasta temporária onde os arquivos JSON e informações auxiliares são armazenados.

## Observações

- Certifique-se de fazer um backup dos seus arquivos MKV antes de executar o script, pois as alterações serão feitas diretamente nesses arquivos.
- Verifique se as ferramentas `mkvmerge` e `mkvpropedit` estão instaladas corretamente e acessíveis pelo caminho (PATH) do sistema.
- Certifique-se de que os arquivos MKV contenham faixas de áudio e/ou legendas para que as alterações sejam aplicadas corretamente.

Divirta-se editando suas faixas MKV com facilidade! 😄🎬
