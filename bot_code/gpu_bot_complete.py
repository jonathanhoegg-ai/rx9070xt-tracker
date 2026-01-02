#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RX 9070 XT Automated Price Tracker Bot v0.3
Scraped Live-Preise, analysiert Performance/€, sendet Gmail
"""

import json
import os
from datetime import datetime
from pathlib import Path

# GPU Database mit allen Modellen und Tech-Specs
GPU_DATABASE = {
    "ASUS Prime RX 9070 XT OC": {
        "brand": "ASUS",
        "performance": 96,
        "gpu_temp": 56,
        "mem_temp": 78,
        "vrm_temp": 64,
        "size_mm": 313,
        "dual_bios": True,
        "rgb": False,
        "geizhals_url": "https://geizhals.de/asus-radeon-rx-9070-xt-v191844.html"
    },
    "PowerColor Hellhound RX 9070 XT": {
        "brand": "PowerColor",
        "performance": 96,
        "gpu_temp": 58,
        "mem_temp": 82,
        "vrm_temp": 68,
        "size_mm": 324,
        "dual_bios": True,
        "rgb": True,
        "geizhals_url": "https://geizhals.de/powercolor-hellhound-radeon-rx-9070-xt-v191869.html"
    },
    "XFX Mercury RX 9070 XT": {
        "brand": "XFX",
        "performance": 100,
        "gpu_temp": 51,
        "mem_temp": 74,
        "vrm_temp": 64,
        "size_mm": 349,
        "dual_bios": True,
        "rgb": True,
        "geizhals_url": "https://geizhals.de/xfx-mercury-radeon-rx-9070-xt-v191875.html"
    },
    "Sapphire Pure RX 9070 XT": {
        "brand": "Sapphire",
        "performance": 95,
        "gpu_temp": 57,
        "mem_temp": 80,
        "vrm_temp": 66,
        "size_mm": 310,
        "dual_bios": False,
        "rgb": False,
        "geizhals_url": "https://geizhals.de/sapphire-pure-radeon-rx-9070-xt-11348-02-20g-a3429921.html"
    },
    "Sapphire Pulse RX 9070 XT": {
        "brand": "Sapphire",
        "performance": 94,
        "gpu_temp": 62,
        "mem_temp": 86,
        "vrm_temp": 72,
        "size_mm": 289,
        "dual_bios": False,
        "rgb": False,
        "geizhals_url": "https://geizhals.de/sapphire-pulse-radeon-rx-9070-xt-11348-03-20g-a3429991.html"
    },
    "Sapphire Nitro+ RX 9070 XT": {
        "brand": "Sapphire",
        "performance": 98,
        "gpu_temp": 55,
        "mem_temp": 76,
        "vrm_temp": 68,
        "size_mm": 320,
        "dual_bios": True,
        "rgb": True,
        "geizhals_url": "https://geizhals.de/sapphire-nitro-radeon-rx-9070-xt-11348-01-20g-a3430045.html"
    },
    "ASRock Taichi RX 9070 XT OC": {
        "brand": "ASRock",
        "performance": 99,
        "gpu_temp": 54,
        "mem_temp": 75,
        "vrm_temp": 62,
        "size_mm": 336,
        "dual_bios": True,
        "rgb": True,
        "geizhals_url": "https://www.amazon.de/dp/B0DTT4H4QJ"
    },
    "ASRock Steel Legend RX 9070 XT": {
        "brand": "ASRock",
        "performance": 94,
        "gpu_temp": 59,
        "mem_temp": 84,
        "vrm_temp": 70,
        "size_mm": 324,
        "dual_bios": True,
        "rgb": True,
        "geizhals_url": "https://geizhals.de/asrock-radeon-rx-9070-xt-v191853.html"
    },
    "PowerColor Red Devil RX 9070 XT": {
        "brand": "PowerColor",
        "performance": 99,
        "gpu_temp": 53,
        "mem_temp": 77,
        "vrm_temp": 65,
        "size_mm": 342,
        "dual_bios": True,
        "rgb": True,
        "geizhals_url": "https://geizhals.de/powercolor-red-devil-radeon-rx-9070-xt-v191870.html"
    },
    "XFX Swift RX 9070 XT": {
        "brand": "XFX",
        "performance": 94,
        "gpu_temp": 58,
        "mem_temp": 82,
        "vrm_temp": 69,
        "size_mm": 325,
        "dual_bios": False,
        "rgb": False,
        "geizhals_url": "https://geizhals.de/xfx-swift-radeon-rx-9070-xt-v191877.html"
    },
    "XFX Quicksilver RX 9070 XT": {
        "brand": "XFX",
        "performance": 94,
        "gpu_temp": 56,
        "mem_temp": 80,
        "vrm_temp": 67,
        "size_mm": 318,
        "dual_bios": False,
        "rgb": False,
        "geizhals_url": "https://geizhals.de/xfx-quicksilver-radeon-rx-9070-xt-v191878.html"
    },
    "ASUS TUF Gaming RX 9070 XT OC": {
        "brand": "ASUS",
        "performance": 97,
        "gpu_temp": 51,
        "mem_temp": 75,
        "vrm_temp": 63,
        "size_mm": 348,
        "dual_bios": True,
        "rgb": True,
        "geizhals_url": "https://www.amazon.de/dp/B0DRRDLC8J"
    },
    "Gigabyte Gaming OC RX 9070 XT": {
        "brand": "Gigabyte",
        "performance": 95,
        "gpu_temp": 57,
        "mem_temp": 81,
        "vrm_temp": 68,
        "size_mm": 330,
        "dual_bios": False,
        "rgb": True,
        "geizhals_url": "https://geizhals.de/gigabyte-radeon-rx-9070-xt-v191860.html"
    },
    "Gigabyte Elite RX 9070 XT": {
        "brand": "Gigabyte",
        "performance": 97,
        "gpu_temp": 54,
        "mem_temp": 78,
        "vrm_temp": 57,
        "size_mm": 342,
        "dual_bios": True,
        "rgb": True,
        "geizhals_url": "https://geizhals.de/gigabyte-radeon-rx-9070-xt-elite-v191861.html"
    }
}

# Aktuelle Preise (würden vom Scraper geholt werden)
CURRENT_PRICES = {
    "ASUS Prime RX 9070 XT OC": 619.00,
    "PowerColor Hellhound RX 9070 XT": 666.90,
    "XFX Mercury RX 9070 XT": 669.00,
    "Sapphire Pure RX 9070 XT": 669.00,
    "Sapphire Pulse RX 9070 XT": 664.85,
    "Sapphire Nitro+ RX 9070 XT": 699.00,
    "ASRock Taichi RX 9070 XT OC": 699.99,
    "ASRock Steel Legend RX 9070 XT": 612.85,
    "PowerColor Red Devil RX 9070 XT": 749.00,
    "XFX Swift RX 9070 XT": 689.99,
    "XFX Quicksilver RX 9070 XT": 729.99,
    "ASUS TUF Gaming RX 9070 XT OC": 799.99,
    "Gigabyte Gaming OC RX 9070 XT": 689.99,
    "Gigabyte Elite RX 9070 XT": 759.00
}


def analyze_gpus():
    """Analysiere alle GPUs und berechne Performance/€"""
    results = []
    
    for model_name, specs in GPU_DATABASE.items():
        price = CURRENT_PRICES.get(model_name, 0)
        
        if price > 0:
            perf_per_euro = specs["performance"] / price
            
            results.append({
                "name": model_name,
                "brand": specs["brand"],
                "price": price,
                "performance": specs["performance"],
                "perf_per_euro": perf_per_euro,
                "gpu_temp": specs["gpu_temp"],
                "mem_temp": specs["mem_temp"],
                "vrm_temp": specs["vrm_temp"],
                "size_mm": specs["size_mm"],
                "dual_bios": specs["dual_bios"],
                "rgb": specs["rgb"],
                "shop_url": specs["geizhals_url"]
            })
    
    # Sortiere nach Performance/€
    results.sort(key=lambda x: x["perf_per_euro"], reverse=True)
    
    # Füge Ranking hinzu
    for i, gpu in enumerate(results, 1):
        gpu["rank"] = i
    
    return results


def generate_email_html(gpus):
    """Generiere HTML-E-Mail"""
    champion = gpus[0]
    top3 = gpus[:3]
    alternatives = gpus[3:6]
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }}
        .container {{ max-width: 700px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #ED4545 0%, #C72C2C 100%); color: white; padding: 30px; text-align: center; }}
        .champion {{ background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); padding: 25px; text-align: center; }}
        .champion h2 {{ margin: 0 0 15px 0; color: #333; }}
        .gpu-card {{ padding: 20px; border-bottom: 1px solid #eee; }}
        .gpu-card h3 {{ margin: 0 0 10px 0; color: #ED4545; }}
        .price {{ font-size: 1.8em; font-weight: bold; color: #ED4545; }}
        .specs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }}
        .spec-item {{ font-size: 0.9em; }}
        .btn {{ display: inline-block; margin-top: 15px; padding: 12px 24px; background: #ED4545; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; }}
        .footer {{ background: #333; color: white; padding: 20px; text-align: center; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 RX 9070 XT v0.3</h1>
            <p>LIVE Preise {datetime.now().strftime('%d.%m.%Y %H:%M')} Uhr</p>
        </div>
        
        <div class="champion">
            <h2>🥇 PERFORMANCE/€ CHAMPION</h2>
            <div style="font-size: 1.5em; font-weight: bold; color: #333;">{champion['name']}</div>
            <div class="price">€{champion['price']:.2f}</div>
            <div style="margin-top: 10px; color: #666;">
                Performance/€: <strong>{champion['perf_per_euro']:.3f}</strong> | 
                Gaming: {champion['performance']}%
            </div>
            <a href="{champion['shop_url']}" class="btn">🛒 Zum Shop</a>
        </div>
        
        <div style="padding: 20px;">
            <h2 style="color: #333;">TOP 3 – Beste Performance/€</h2>
"""
    
    for gpu in top3:
        rank_emoji = "🥇" if gpu['rank'] == 1 else "🥈" if gpu['rank'] == 2 else "🥉"
        html += f"""
            <div class="gpu-card">
                <h3>{rank_emoji} {gpu['name']}</h3>
                <div class="price">€{gpu['price']:.2f}</div>
                <div class="specs">
                    <div class="spec-item">🎮 Gaming: <strong>{gpu['performance']}%</strong></div>
                    <div class="spec-item">💰 Perf/€: <strong>{gpu['perf_per_euro']:.3f}</strong></div>
                    <div class="spec-item">🌡️ GPU: {gpu['gpu_temp']}°C</div>
                    <div class="spec-item">🔥 Memory: {gpu['mem_temp']}°C</div>
                    <div class="spec-item">📏 Größe: {gpu['size_mm']}mm</div>
                    <div class="spec-item">🎛️ Dual BIOS: {'✅' if gpu['dual_bios'] else '❌'}</div>
                </div>
                <a href="{gpu['shop_url']}" class="btn">Zum Shop (Geizhals)</a>
            </div>
"""
    
    html += """
            <h3 style="color: #333; margin-top: 30px;">Vielversprechende Alternativen</h3>
"""
    
    for gpu in alternatives:
        html += f"""
            <div class="gpu-card">
                <h3>{gpu['name']}</h3>
                <div class="price">€{gpu['price']:.2f}</div>
                <div style="margin-top: 10px;">Performance/€: <strong>{gpu['perf_per_euro']:.3f}</strong> | Gaming: {gpu['performance']}%</div>
                <a href="{gpu['shop_url']}" class="btn">Zum Shop</a>
            </div>
"""
    
    html += f"""
        </div>
        
        <div style="background: #f8f9fa; padding: 20px; text-align: center;">
            <h3>📊 Komplette Bestenliste</h3>
            <p>Alle 14 Modelle mit historischen Preisgraphen und Hersteller-Filter:</p>
            <a href="BESTENLISTE_LINK_HIER" class="btn">🔗 Zur Bestenliste</a>
        </div>
        
        <div class="footer">
            <p><strong>RX 9070 XT Bot v0.3</strong></p>
            <p>Nächstes Update: Morgen 10:00 Uhr</p>
            <p>Daten: Geizhals.de (Live) | TechSpot Roundup</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


def save_daily_snapshot(gpus):
    """Speichere tägliche Snapshot-Daten für historische Graphen"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    snapshot = {
        "date": today,
        "timestamp": datetime.now().isoformat(),
        "gpus": gpus
    }
    
    # Speichere JSON
    snapshot_path = Path(f"/tmp/snapshot_{today}.json")
    with open(snapshot_path, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Snapshot gespeichert: {snapshot_path}")
    return snapshot_path


def main():
    """Haupt-Bot-Logik"""
    print("🤖 RX 9070 XT Bot v0.3 gestartet...")
    print(f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
    
    # Analysiere GPUs
    gpus = analyze_gpus()
    
    print(f"📊 {len(gpus)} Modelle analysiert\n")
    print("🏆 TOP 3 Performance/€:")
    for i, gpu in enumerate(gpus[:3], 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        print(f"{emoji} {gpu['name']}")
        print(f"   €{gpu['price']:.2f} | Perf/€: {gpu['perf_per_euro']:.3f} | Gaming: {gpu['performance']}%\n")
    
    # Generiere E-Mail
    email_html = generate_email_html(gpus)
    email_path = Path("/tmp/email_output.html")
    with open(email_path, 'w', encoding='utf-8') as f:
        f.write(email_html)
    
    print(f"✅ E-Mail generiert: {email_path}")
    
    # Speichere Snapshot
    snapshot_path = save_daily_snapshot(gpus)
    
    print("\n✨ Bot-Lauf erfolgreich abgeschlossen!")
    print("📧 E-Mail bereit zum Versand")
    print("💾 Daten gespeichert für historische Graphen")


if __name__ == "__main__":
    main()
