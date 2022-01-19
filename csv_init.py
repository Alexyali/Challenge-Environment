import csv

result_csv_path = "result.csv"

with open(result_csv_path, 'w', encoding='utf8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["CC", "COND", "avg_qdelay", "95%_qdelay", "avg_tput", "loss_rate", "ssrc"])
