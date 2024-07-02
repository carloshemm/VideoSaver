#!/bin/bash

# Obtém o diretório atual
DIR=$(pwd)

# Obtém o caminho do Python
PYTHON_PATH=$(which python3)

# Nome do novo arquivo bash a ser criado
BASH_FILE="runVideoSaver.sh"

# Cria o novo arquivo bash com o comando para executar videoSaver.py
echo "#!/bin/bash" > $BASH_FILE
echo "$PYTHON_PATH $DIR/videoSaver.py --time INT --input STR"  >> $BASH_FILE

# Torna o novo arquivo bash executável
chmod +x $BASH_FILE

echo "Setup completo. Use ./$BASH_FILE para executar videoSaver.py"

echo ""

# Nome do arquivo cron
CRON_FILE="videoSaverCron"

# Cria ou atualiza o arquivo cron com a tarefa
echo "0 9-21 * * * $DIR/$BASH_FILE" > $CRON_FILE

# Instruções para configurar manualmente a tarefa cron
echo "Para configurar a tarefa cron, execute: crontab $CRON_FILE"
echo "Arquivo de tarefa cron criado: $CRON_FILE"