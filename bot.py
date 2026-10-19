import os

import requests

from datetime import datetime



# --- CARREGA O WEBHOOK DE FORMA SEGURA DO GITHUB SECRETS ---

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")



def fetch_usd_brl_rate():

    try:

        resp = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL", timeout=5)

        if resp.status_code == 200:

            return float(resp.json().get("USDBRL", {}).get("bid", 5.50))

    except Exception:

        pass

    return 5.50



def fetch_market_data():

    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 5, "page": 1, "sparkline": "false"}

    try:

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:

            return response.json()

    except Exception:

        pass

    return []



def fetch_memecoin_data():

    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {"vs_currency": "usd", "category": "meme-token", "order": "market_cap_desc", "per_page": 20, "page": 1, "sparkline": "false"}

    try:

        response = requests.get(url, params=params, timeout=15)

        if response.status_code == 200:

            return response.json()

    except Exception:

        pass

    return []



def send_discord_webhook(text_content):

    if not DISCORD_WEBHOOK_URL:

        print("[!] DISCORD_WEBHOOK_URL não configurado.")

        return False



    try:

        chunk_size = 1900

        chunks = [text_content[i:i + chunk_size] for i in range(0, len(text_content), chunk_size)]



        for chunk in chunks:

            payload = {"content": f"```markdown\n{chunk}\n```"}

            requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)

        print("[OK] Relatório enviado com sucesso para o Discord!")

        return True

    except Exception as e:

        print(f"[!] Erro ao enviar para o Discord: {e}")

        return False



def main():

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando varredura (5 Institucionais + 20 Memes)...")

    

    usd_brl = fetch_usd_brl_rate()

    coins = fetch_market_data()

    memecoins = fetch_memecoin_data()

    

    if not coins and not memecoins:

        print("[!] Falha ao obter dados das criptomoedas.")

        return



    report_lines = [

        "=== 🛡️ RELATÓRIO: TOP 5 INSTITUCIONAIS ===",

        f"Câmbio USD/BRL: R$ {usd_brl:.2f}\n",

        f"{'Rank':<4} {'Ativo':<8} {'Preço USD':<12} {'Preço BRL':<12} {'Var 24h':<8}",

        "-" * 50

    ]



    for idx, c in enumerate(coins, 1):

        p_usd = c.get('current_price') or 0

        p_brl = p_usd * usd_brl

        var = c.get('price_change_percentage_24h') or 0

        sym = c.get('symbol', '').upper()

        report_lines.append(f"{idx:<4} {sym:<8} ${p_usd:<11,.2f} R$ {p_brl:<11,.2f} {var:>+6.2f}%")



    report_lines.append("\n=== 🐶 RADAR: TOP 20 MEMECOINS ===")

    report_lines.append(f"{'Rank':<4} {'Meme':<8} {'Preço USD':<12} {'Preço BRL':<12} {'Var 24h':<8}")

    report_lines.append("-" * 50)



    for idx, m in enumerate(memecoins, 1):

        p_usd = m.get('current_price') or 0

        p_brl = p_usd * usd_brl

        str_usd = f"${p_usd:.6f}" if p_usd < 0.01 else f"${p_usd:,.2f}"

        str_brl = f"R$ {p_brl:.6f}" if p_brl < 0.01 else f"R$ {p_brl:,.2f}"

        var = m.get('price_change_percentage_24h') or 0

        sym = m.get('symbol', '').upper()

        report_lines.append(f"{idx:<4} {sym:<8} {str_usd:<12} {str_brl:<12} {var:>+6.2f}%")



    full_report = "\n".join(report_lines)

    send_discord_webhook(full_report)



if __name__ == "__main__":

    main() 
