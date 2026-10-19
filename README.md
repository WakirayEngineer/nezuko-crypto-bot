Nezuko Crypto Bot 🛡️🤖
Um bot automatizado desenvolvido em Python para monitorização de criptomoedas, integrado com o GitHub Actions para envio de relatórios periódicos diretamente para um canal do Discord.

Funcionalidades
Varredura de Ativos: Analisa o top de ativos institucionais e o radar de memecoins utilizando os dados do CoinGecko e indicadores da Binance.

Cotação em Tempo Real: Converte e exibe os valores em USD e BRL (utilizando a cotação oficial).

Automação na Nuvem: Executa de forma programada a cada 1 hora através do GitHub Actions, sem necessidade de manter nenhum computador ligado.

Estrutura do Repositório
bot.py — Script principal em Python responsável por recolher os dados, processar os relatórios e disparar o webhook.

.github/workflows/bot.yml — Ficheiro de configuração responsável por automatizar a execução horária na nuvem do GitHub.

Configuração e Segurança
Para garantir a segurança das tuas chaves, o bot utiliza os GitHub Secrets (DISCORD_WEBHOOK_URL), mantendo o link do Webhook do Discord totalmente protegido e oculto no código público.
