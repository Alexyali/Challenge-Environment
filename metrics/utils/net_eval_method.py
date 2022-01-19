#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.net_info import NetInfo
import numpy as np
from abc import ABC, abstractmethod
import csv
# import json
import matplotlib.pyplot as plt

delay_log_path = "/home/alex/Challenge-Environment/paper_result/cldcc_delay.log"
tput_log_path = "/home/alex/Challenge-Environment/paper_result/cldcc_tput.log"
result_csv_path = "/home/alex/Challenge-Environment/result.csv"
condition = "none"
algorithm = "RTC-CLDCC"

class NetEvalMethod(ABC):
    @abstractmethod
    def __init__(self):
        self.eval_name = "base"

    @abstractmethod
    def eval(self, dst_audio_info : NetInfo):
        pass


class NetEvalMethodNormal(NetEvalMethod):
    def __init__(self, max_delay=400, ground_recv_rate=500):
        super(NetEvalMethodNormal, self).__init__()
        self.eval_name = "normal"
        self.max_delay = max_delay
        self.ground_recv_rate = ground_recv_rate

    def eval(self, dst_audio_info : NetInfo):
        net_data = dst_audio_info.net_data
        ssrc_info = {}

        delay_list = []
        loss_count = 0
        self.last_seqNo = {}
        for item in net_data:
            ssrc = item["packetInfo"]["header"]["ssrc"]
            sequence_number = item["packetInfo"]["header"]["sequenceNumber"]
            tmp_delay = item["packetInfo"]["arrivalTimeMs"] - item["packetInfo"]["header"]["sendTimestamp"]
            if (ssrc not in ssrc_info):
                ssrc_info[ssrc] = {
                    "time_delta" : -tmp_delay,
                    "delay_list" : [],
                    "received_nbytes" : 0,
                    "start_recv_time" : item["packetInfo"]["arrivalTimeMs"],
                    "first_recv_time" : item["packetInfo"]["arrivalTimeMs"],
                    "recv_rate" : [],
                    "recv_timestamp" : []
                }
            if ssrc in self.last_seqNo:
                loss_count += max(0, sequence_number - self.last_seqNo[ssrc] - 1)
            self.last_seqNo[ssrc] = sequence_number

            ssrc_info[ssrc]["delay_list"].append(ssrc_info[ssrc]["time_delta"] + tmp_delay)
            ssrc_info[ssrc]["recv_timestamp"].append((item["packetInfo"]["arrivalTimeMs"]-ssrc_info[ssrc]["first_recv_time"])/1000.0)
            ssrc_info[ssrc]["received_nbytes"] += item["packetInfo"]["payloadSize"]
            if item["packetInfo"]["arrivalTimeMs"] != ssrc_info[ssrc]["start_recv_time"] and (item["packetInfo"]["arrivalTimeMs"] - ssrc_info[ssrc]["start_recv_time"]) > 1000:
                ssrc_info[ssrc]["recv_rate"].append(ssrc_info[ssrc]["received_nbytes"] / (item["packetInfo"]["arrivalTimeMs"] - ssrc_info[ssrc]["start_recv_time"])*8)
                ssrc_info[ssrc]["start_recv_time"] = item["packetInfo"]["arrivalTimeMs"]
                ssrc_info[ssrc]["received_nbytes"] = 0

        # scale delay list
        for ssrc in ssrc_info:
            min_delay = min(ssrc_info[ssrc]["delay_list"])
            ssrc_info[ssrc]["scale_delay_list"] = [min(self.max_delay, delay) for delay in ssrc_info[ssrc]["delay_list"]]
            delay_pencentile_95 = np.percentile(ssrc_info[ssrc]["scale_delay_list"], 95)
            ssrc_info[ssrc]["delay_score"] = (self.max_delay - delay_pencentile_95) / (self.max_delay - min_delay)
        # delay score
        avg_delay_score = np.mean([np.mean(ssrc_info[ssrc]["delay_score"]) for ssrc in ssrc_info])

        # receive rate score
        recv_rate_list = [np.mean(ssrc_info[ssrc]["recv_rate"]) for ssrc in ssrc_info]
        avg_recv_rate_score = min(1, np.mean(recv_rate_list) / self.ground_recv_rate)

        # higher loss rate, lower score
        avg_loss_rate = loss_count / (loss_count + len(net_data))

        # calculate result score
        network_score = 100 * 0.2 * avg_delay_score + \
                            100 * 0.2 * avg_recv_rate_score + \
                            100 * 0.3 * (1 - avg_loss_rate)

        for ssrc in ssrc_info:
            if len(ssrc_info[ssrc]["delay_list"]) < 10:
                continue
            #f = open("result/ssrc_" + str(ssrc) + ".log", "w")
            ssrc_info[ssrc]["avg_loss_rate"] = avg_loss_rate
            ssrc_info[ssrc]["avg_recv_rate_score"] = avg_recv_rate_score
            ssrc_info[ssrc]["avg_delay_score"] = avg_delay_score
            ssrc_info[ssrc]["network_score"] = network_score
            #f.write(json.dumps(ssrc_info[ssrc]))
            #f.close()
            print("ssrc:", ssrc)

            plt.figure()
            plt.grid()
            min_delay = np.min(ssrc_info[ssrc]["delay_list"])
            with open(delay_log_path,"w") as f:
                f.write("ssrc=%s\n" %(str(ssrc)))
                for i in range(len(ssrc_info[ssrc]["delay_list"])):
                    f.write("time: %.3f qdelay: %d\n" %(ssrc_info[ssrc]["recv_timestamp"][i], ssrc_info[ssrc]["delay_list"][i]-min_delay))
            plt.plot(ssrc_info[ssrc]["recv_timestamp"], [i-min_delay for i in ssrc_info[ssrc]["delay_list"]])
            plt.ylabel("queue delay/ms", fontsize=14)
            plt.xlabel("time/s", fontsize=14)
            plt.tick_params(labelsize=16)
            delay_pencentile_95 = np.percentile(ssrc_info[ssrc]["delay_list"], 95, interpolation="nearest")
            avg_delay = np.average(ssrc_info[ssrc]["delay_list"])

            print("delay_95%:", delay_pencentile_95-min_delay,"ms")
            print("avg_delay:", round(avg_delay-min_delay,3),"ms")
            plt.title("avg_qdelay="+str(round(avg_delay-min_delay,3))+"ms",fontsize=14)
            #plt.savefig("result/ssrc_" + str(ssrc) + "_delay.png")

            plt.figure()
            plt.plot(ssrc_info[ssrc]["recv_rate"])
            with open(tput_log_path,"w") as f:
                f.write("ssrc=%s\n" %(str(ssrc)))
                for i in ssrc_info[ssrc]["recv_rate"]:
                    f.write("%.3f\n" %(i))
            plt.grid()
            plt.ylabel("receive rate/kbps",fontsize=14)
            plt.xlabel("time/s",fontsize=14)
            plt.tick_params(labelsize=12)
            plt.title("avg_throughput="+str(round(np.mean(ssrc_info[ssrc]["recv_rate"]), 3))+"kbps",fontsize=14)
            print("avg throughput:", round(np.mean(ssrc_info[ssrc]["recv_rate"]), 3),"kbps")
            #plt.savefig("result/ssrc_" + str(ssrc) + "_rate.png")

            with open(result_csv_path, 'a', encoding='utf8') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow([
                   algorithm,
                   condition,
                   round(avg_delay-min_delay,3),
                   delay_pencentile_95-min_delay,
                   round(np.mean(ssrc_info[ssrc]["recv_rate"]), 3),
                   round(ssrc_info[ssrc]["avg_loss_rate"], 2),
                   ssrc
                ])
        return network_score