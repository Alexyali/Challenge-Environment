import argparse
import matplotlib.pyplot as plt

# draw delay figure

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

def draw_delay_fig(cc_list:list, data_dir:str):

    plt.figure(figsize=(12,5))
    for cc in cc_list:
        delay_log_path = data_dir + cc + "_delay.log"
        delay_list = []
        timestamp_list = []
        delay_list, timestamp_list = get_delay_list(delay_log_path)
        plt.plot(timestamp_list, delay_list, label=cc)

    plt.grid()
    plt.legend(fontsize=15)
    plt.tick_params(labelsize=14)
    plt.xlabel("time/s", fontsize=15)
    plt.ylabel("queue delay/ms", fontsize=15)
    plt.savefig(data_dir + "cmp_delay.png", dpi=300)
    plt.close()

# draw throughput figure

def get_tput_list(log_file:str):
    tput_list = []
    with open(log_file, "r") as f:
        f.readline()
        lines = f.readlines()
        for row in lines:
            data = row.strip()
            tput_list.append(float(data))
    return tput_list

def draw_tput_fig(cc_list:list, data_dir:str):

    plt.figure(figsize=(12,5))
    for cc in cc_list:
        tput_log_path = data_dir + cc + "_tput.log"
        tput_list = get_tput_list(tput_log_path)
        plt.plot(tput_list, label=cc)

    plt.grid()
    plt.legend(fontsize=15)
    plt.tick_params(labelsize=14)
    plt.xlabel("time/s", fontsize=15)
    plt.ylabel("throughput/kbps", fontsize=15)
    plt.savefig(data_dir + "cmp_tput.png", dpi=300)
    plt.close()

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schemes", type=str, required=True, help="congestion control schemes, such as gcc or cldcc")
    parser.add_argument("--data_dir", type=str, default=None, required=True, help="data folder")

    return parser

if __name__ == "__main__":
    parser = init_args()
    args = parser.parse_args()
    cc_list = args.schemes
    cc_list = cc_list.strip().split()
    draw_delay_fig(cc_list, args.data_dir)
    draw_tput_fig(cc_list, args.data_dir)
