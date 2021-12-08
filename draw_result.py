import matplotlib.pyplot as plt

# draw combine delay_list

gcc_delay_log = "paper_result/gcc_delay.log"
cldcc_delay_log = "paper_result/cldcc_delay.log"

gcc_tput_log = "paper_result/gcc_tput.log"
cldcc_tput_log = "paper_result/cldcc_tput.log"

gcc_delay_list = []
cldcc_delay_list = []
gcc_recv_timestamp = []
cldcc_recv_timestamp = []

with open(gcc_delay_log, "r") as f:
    f.readline()
    lines = f.readlines()
    for row in lines:
        data = row.strip().split()
        gcc_delay_list.append(int(data[-1]))
        gcc_recv_timestamp.append(float(data[1]))

with open(cldcc_delay_log, "r") as f:
    f.readline()
    lines = f.readlines()
    for row in lines:
        data = row.strip().split()
        cldcc_delay_list.append(int(data[-1]))
        cldcc_recv_timestamp.append(float(data[1]))

plt.figure(figsize=(12,5))

plt.plot(gcc_recv_timestamp, gcc_delay_list,color="red",label="Trendline-GCC")
plt.plot(cldcc_recv_timestamp, cldcc_delay_list,color="blue", label="RTC-CLDCC")
plt.legend(fontsize=15)
plt.grid()
plt.tick_params(labelsize=14)
plt.xlabel("time/s", fontsize=15)
plt.ylabel("queue delay/ms", fontsize=15)
plt.savefig("paper_result/test_delay.png", dpi=300)
plt.close()

# draw throughput
gcc_tput_list = []
cldcc_tput_list = []
with open(gcc_tput_log, "r") as f:
    f.readline()
    lines = f.readlines()
    for row in lines:
        data = row.strip()
        gcc_tput_list.append(float(data))

with open(cldcc_tput_log, "r") as f:
    f.readline()
    lines = f.readlines()
    for row in lines:
        data = row.strip()
        cldcc_tput_list.append(float(data))

plt.figure(figsize=(12,5))

plt.plot(gcc_tput_list,color="red",label="Trendline-GCC")
plt.plot(cldcc_tput_list,color="blue", label="RTC-CLDCC")
plt.legend(fontsize=15)
plt.grid()
plt.tick_params(labelsize=14)
plt.xlabel("time/s", fontsize=15)
plt.ylabel("throughput/kbps", fontsize=15)
plt.savefig("paper_result/test_tput.png", dpi=300)
plt.close()