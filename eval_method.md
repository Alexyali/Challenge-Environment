# 测试方法

该分支是为了分析`peerconnection_alphartc`运行生成的`webrtc.log`日志，并导出网络性能指标和结果比较图表。

## 准备

- 首先将`Challenge-Environment`克隆到和`peerconnection_alphartc`仓库相同的目录下。

- 根据`peerconnection_alphartc`的README运行实时视频传输demo。运行完成后在`peerconnection_alphartc/result`目录下会生成`webrtc.log`日志文件。

## 安装依赖

python3需要支持`soundfile`。

```shell
$ pip3 install soundfile
```

## 数据分析

1. 初始化`result.csv`用于保存实验数据。

```shell
$ python3 csv_init.py
```

运行上述指令后将生成包括指标名称的`result.csv`文件。

注意：只需要初始化一次，否则会清空之前所有记录的数据。

2. 分析`webrtc.log`，将对应的吞吐量和延迟日志保存在`paper_result`目录下，并且将对应指标写入`result.csv`中。在`eval.sh`中可以修改测试的算法（gcc或者cldcc）和运行条件等参数。

```shell
# make dir to store result
$ mkdir paper_result

# run script for evaluation
$ sh eval.sh
```

## 对比不同算法

`peerconnection_alphartc`仓库支持GCC算法和CLDCC算法，分别使用不同的Estimator实现。

- 为了对比这两个算法，分别在`peerconnection_alphartc`下运行不同算法，每运行一种算法就执行`eval.sh`，以生成相应的日志文件。

注意：切换算法后需要修改`eval.sh`中的`--algo`选项，选择`gcc`或者`cldcc`。

```shell
# after run peerconnection used gcc
$ sh eval.sh

# after run peerconnection used cldcc
# change `algo` to `cldcc` in `eval.sh`
$ sh eval.sh
```

- 分别运行两次`eval.sh`后，在`paper_result`目录下可以看到gcc和cldcc算法的吞吐量日志以及延迟日志（一共4个文件）。

- 运行`draw_result.py`，分别导出gcc和cldcc算法的延迟对比图和吞吐量对比图，并保存在`paper_result`目录下。

```shell
$ python3 draw_result.py
```