# VideoSaver

O `videoSaver.py` é um script utilizado para gravar vídeos e salvá-los na pasta `VIDEOS/`. Este script aceita vários parâmetros para controlar seu comportamento:

- `--input`: Especifica a URL de entrada do vídeo a ser gravado.
- `--time`: Define o tempo de gravação em minutos.
- `--show`: Quando utilizado, exibe o stream atual sendo gravado.

## Configuração Inicial

O script `setup.sh` é utilizado para configurar o ambiente necessário para executar o `videoSaver.py`. Este processo de configuração inclui a criação de tarefas cron para automatizar a execução do script `videoSaver.py` em intervalos regulares.

### Modificação de Parâmetros

Para personalizar os parâmetros de entrada (`--input`) e o tempo de gravação (`--time`), é necessário modificar o arquivo `runVideoSaver.sh`. Este arquivo é utilizado pelo `setup.sh` para agendar a execução do `videoSaver.py` com os parâmetros especificados. Certifique-se de ajustar esses parâmetros conforme necessário antes de executar o `setup.sh`.