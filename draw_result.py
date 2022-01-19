import matplotlib.pyplot as plt

# draw delay_list

gcc_delay_log = "paper_result/gcc_delay.log"
cldcc_delay_log = "paper_result/cldcc_delay.log"

gcc_tput_log = "paper_result/gcc_tput.log"
cldcc_tput_log = "paper_result/cldcc_tput.log"

def get_delay_list(log_file:str):
    delay = []
    recv_rate = []
    with open(log_file, "r") as f:
        f.readline()
        lines = f.readlines()
        for row in lines:
            data = row.strip().split()
            delay.append(int(data[-1]))
            recv_rate.append(float(data[1]))
    return delay, recv_rate

gcc_delay_list = []
gcc_recv_timestamp = []
gcc_delay_list, gcc_recv_timestamp = get_delay_list(gcc_delay_log)

cldcc_delay_list = []
cldcc_recv_timestamp = []
cldcc_delay_list, cldcc_recv_timestamp = get_delay_list(cldcc_delay_log)

plt.figure(figsize=(12,5))
plt.plot(gcc_recv_timestamp, gcc_delay_list,color="red",linestyle="--",label="Trendline-GCC")
plt.plot(cldcc_recv_timestamp, cldcc_delay_list,color="blue", label="RTC-CLDCC")
plt.legend(fontsize=15)
plt.grid()
plt.tick_params(labelsize=14)
plt.xlabel("time/s", fontsize=15)
plt.ylabel("queue delay/ms", fontsize=15)
plt.savefig("paper_result/test_delay.png", dpi=300)
plt.close()

# draw throughput

def get_tput_list(log_file:str):
    tput_list = []
    with open(log_file, "r") as f:
        f.readline()
        lines = f.readlines()
        for row in lines:
            data = row.strip()
            tput_list.append(float(data))
    return tput_list

gcc_tput_list = []
gcc_tput_list = get_tput_list(gcc_tput_log)

cldcc_tput_list = []
cldcc_tput_list = get_tput_list(cldcc_tput_log)

plt.figure(figsize=(12,5))
plt.plot(gcc_tput_list,color="red",linestyle="--",label="Trendline-GCC")
plt.plot(cldcc_tput_list,color="blue", label="RTC-CLDCC")
plt.legend(fontsize=15)
plt.grid()
plt.tick_params(labelsize=14)
plt.xlabel("time/s", fontsize=15)
plt.ylabel("throughput/kbps", fontsize=15)
plt.savefig("paper_result/test_tput.png", dpi=300)
plt.close()