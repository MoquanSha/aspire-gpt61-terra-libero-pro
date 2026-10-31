# ASPIRE × GPT-6.1-terra 在 LIBERO-Pro 上的复现记录

用 [NVlabs/ASPIRE](https://github.com/NVlabs/ASPIRE)（commit `fa00f0e`）原版的 iterative-debugging 协议，让 Codex CLI 0.166.0 + `gpt-6.1-terra` 从零写机器人控制程序（Code-as-Policy），在 LIBERO-Pro 仿真中自己调试、自己验证。四个任务都在同一个干净的 campaign 里完成（2026-10-31）。

仓库包含 Codex 写的每一版程序、修改记录、失败分析和逐次试验结果，不包含 ASPIRE 框架本身。全部 828 段仿真视频放在网盘，见[视频](#视频)。

## 结果

| 任务 | 指令 | 版本 | 开发 51–65 | 未见 66–80 | 留出 1–50 |
|---|---|---|---|---|---|
| `libero_object_swap` task 0 | Pick the alphabet soup and place it in the basket | 4（选 v03） | 15/15 | 15/15 | **49/50** |
| `libero_object_swap` task 1 | Pick the cream cheese and place it in the basket | 3（选 v02） | 15/15 | 15/15 | **50/50** |
| `libero_goal_swap` task 0 | Open the middle layer of the drawer | 7（v00–v06） | 0/15 | 未运行 | 未运行 |
| `libero_spatial_swap` task 0 | Pick the akita black bowl between the plate and the ramekin and place it on the plate | 4（v00–v03） | 0/15 | 未运行 | 未运行 |

goal_swap 和 spatial_swap 两个任务，每种失败模式都用完了 3 次修改机会，被记为 blocked。原版协议在 `main-agent-prompt.md` 里规定，第一个开发种子必须成功才能进入未见和留出测试，所以这两个任务按协议在开发阶段结束，算作失败。

所有试验的逐条结果见 [`results/all_trials.csv`](results/all_trials.csv)。

## 和官方公布的模型结果对比

Opus 5.5 和 GPT-6 Astra 的数字取自 ASPIRE 官方 README 的图表（[`assets/official_libero_pro_by_model.png`](assets/official_libero_pro_by_model.png)），这两个模型我没有自己重跑。

| 套件 | Claude Opus 5.5（官方） | GPT-6 Astra（官方） | GPT-6.1 terra（本次） |
|---|---|---|---|
| Object swap | 98.2% | 99.0% | 99%（2 个任务，99/100） |
| Goal swap | 98.0% | 98.2% | task 0 失败（开发 0/15） |
| Spatial swap | 99.4% | 98.4% | task 0 失败（开发 0/15） |

官方数字是整个套件所有任务的平均值，本次每个套件只跑了 1 到 2 个任务，而且只跑了一轮，所以只能粗略参考。官方对比的是 GPT-6 Astra，本次用的是 GPT-6.1 terra。

结论是 terra 在抓起放下这类任务上达到了官方强模型的水平，在需要接触和抓取技巧的任务上明显落后。拉抽屉时它抓不住把手，夹碗时它夹不起比夹爪还宽的碗。

## 每个任务发生了什么

**object_swap task 0。** v00 和 v01 都是运送途中超时，降低路线后又会撞到篮子，0/15。v02 抬高越过篮沿并加了重试，10/15。v03 改用点云 5%–95% 分位包围框的中点来定位篮子，避免可见那面篮壁把中位数拉偏，15/15。Codex 一开始就用 SAM3 试了几种描述，从 v00 起用的就是 "blue soup can"。它提出的"容器中心用包围框中点"这条技能，被 Verifier 用 51–55 两次复现都失败（0/10），判定为 refuted，没有进入技能库。

**object_swap task 1。** v00 夹爪合上后提起，奶酪盒留在原地。v01 往下多伸 2.5 cm，15 个种子全部运动超时。v02 改为只下降 1 cm，15/15，留出 50/50。

**goal_swap task 0。** 执行和接触这个模式，v01 水平接近、v02 伸得更深、v03 旋转夹爪，都是 0/15，被 blocked。感知这个模式，v04 和 v05 放宽了把手置信度，但用到了和场景相关的绝对高度阈值，被来源审计隔离。v06 去掉这个阈值后，程序在 15 个种子上都能完整跑完，但抽屉一次都没拉开。

**spatial_swap task 0。** 碗比夹爪张开的宽度还宽。v00 往碗中心下降时卡住，v01 去夹碗沿，夹爪却空着提了起来，v03 用 contact-graspnet 的候选抓取又出现了 14 次程序错误。v02 由于一次替换没有生效，和 v01 完全一样。这一版也计入了预算，Codex 在 CHANGELOG 里如实记录了这件事。

## 怎么保证这是从零写的

1. 运行前，我把之前所有轮次的结果，以及官方示例程序的运行输出，都移出了 ASPIRE 目录。`skills/`、`.claude/` 和 `.codex/` 与上游 `fa00f0e` 完全一致，Codex 的记忆功能是关闭的。
2. 提示词用的是官方 README Quick Start 的原文，只改了任务列表，并去掉了 clone 和"等待确认"两步。
3. 本次 12 个 Codex 会话共有 1972 次工具调用，我逐条检查过，没有一次读过旧结果、存档或 `examples/libero` 下的官方解法。
4. 所有被选中的程序都通过了非特权 API 审计：只用公开的感知和运动接口，不读仿真器内部状态，也不硬编码坐标。

ASPIRE 的源码里有两处环境兼容补丁，是安装时为了让程序能跑起来而改的，与任务逻辑无关：
- `libero/adapter.py` 里对 init_states 的判空写法
- SAM3 服务改为从本地加载权重

## 运行过程中的意外

这些意外都如实保留了记录，不影响上面的结果，但会影响耗时和 token。

- **额度用完。** 中途 Codex 账号额度用完了。续跑时新开的子代理没有沿用 goal_swap 原有的版本计数，一路写到了 v28，超出了 8 版的预算。按照官方 `clean-task-slate.md` 的规定，我把那次尝试整体归档，goal_swap 从零重跑，上表是重跑的结果。
- **服务器关机。** 关机时 object_swap task 1 的 v00 正在跑开发集。续跑时，已经写完的版本仍然计入预算。

## 耗时与 token

| 任务 | 运行时间段（墙钟） |
|---|---|
| object_swap 0 | 14:35–15:29，约 54 分钟 |
| goal_swap 0（重跑） | 17:05–17:34，约 29 分钟 |
| spatial_swap 0 | 17:34–17:57，约 23 分钟 |
| object_swap 1 | 17:58–18:58，其中包含约 20 分钟的关机中断 |

全部会话加起来一共 111,497,199 token。其中缓存命中 110,269,440，约 98.9%；输出 151,316。这个总数包含了被归档的那次超预算 goal_swap 尝试，约 1450 万。

硬件为 AutoDL 上的单卡 RTX 4090，网络经服务器上的代理连接 OpenAI。

## 视频

网盘链接：**（待补充）**

网盘里的目录结构和 [`results/video_index.csv`](results/video_index.csv) 一一对应：

```
<suite>_task<id>/
  dev_v00 … dev_vNN/     每一版在开发种子 51–65 上的运行
  seed51_precheck_vNN/   正式扫描前在种子 51 上的单次预检
  unseen/                选定版本在未见种子 66–80 上的运行
  heldout/               选定版本在留出种子 1–50 上的运行
  verifier_v01, v02/     Verifier 复现技能的两次尝试（种子 51–55）
    seed<NN>_agentview.mp4   第三人称场景相机
    seed<NN>_wrist.mp4       手腕相机
```

`video_index.csv` 的每一行包含 suite、task_id、phase、version、seed、view、task_success、program_ok、termination_reason、file（网盘内的相对路径）和 source_run（原始运行目录）。

## 局限

- 结果全部来自仿真，每个任务只跑了一轮 Codex，没有统计多次运行之间的方差。
- 每个套件只覆盖了 1 到 2 个任务，和官方的整套件平均值不能直接对比。

## 许可

ASPIRE 由 NVIDIA 以 Apache License 2.0 发布。本仓库中的程序是基于 ASPIRE 公开 API 生成的，同样以 Apache-2.0 发布。
