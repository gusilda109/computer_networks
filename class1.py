import subprocess
import csv
import re

domains = [
    "google.com", "farfetch.com", "yungleantour.com", "macys.com",
    "twitch.com", "ya.ru", "2ch.hk",
    "lurkmore.ru", "tableconvert.com", "kremlin.ru"
]

results = []

for domain in domains:
    process = subprocess.run(
        ["ping", "-c", "4", domain],
        capture_output=True,
        text=True
    )
    output = process.stdout

    loss_match = re.search(r'(\d+)% packet loss', output)
    packet_loss = loss_match.group(1) if loss_match else "N/A"

    rtt_match = re.search(r'rtt .* = ([\d.]+)/([\d.]+)/([\d.]+)/', output)
    if rtt_match:
        rtt_min, rtt_avg, rtt_max = rtt_match.groups()
    else:
        rtt_min = rtt_avg = rtt_max = "N/A"

    results.append([domain, rtt_min, rtt_avg, rtt_max, packet_loss])

with open("rtt.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["domen", "rtt min", "rtt avg", "rtt max", "packet loss %"])
    writer.writerows(results)
