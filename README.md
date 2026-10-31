# ASPIRE × GPT-6.1-terra 在 LIBERO-Pro 上的复现记录

用 [NVlabs/ASPIRE](https://github.com/NVlabs/ASPIRE)（commit `fa00f0e`）的 iterative-debugging 流程，让 Codex CLI 0.166.0 + `gpt-6.1-terra` 从零写机器人控制程序（Code-as-Policy），在 LIBERO-Pro 仿真里自己调试、自己验证。

本仓库只包含 Codex 生成的程序、逐版本修改记录、留出测试的逐种子结果和几段仿真视频，不包含 ASPIRE 框架本身。

## 结果

| 任务 | 指令 | 版本数 | 开发种子 51–65 | 未见检查 66–80 | 留出测试 1–50 |
|---|---|---|---|---|---|
| `libero_object_swap` task 0 | Pick the alphabet soup and place it in the basket | 4（v00–v03） | 15/15 | 15/15 | **50/50** |
| `libero_goal_swap` task 0 | Open the middle layer of the drawer | 8（v00–v07，选 v06） | 7/15 | 6/15 | **25/50** |

- object_swap task 0 的留出测试中，种子 25 任务成功但程序报错退出，程序完整执行率为 49/50。
- goal_swap task 0 的 25 次失败里，22 次是程序报错（运动规划或接触超时），3 次是程序跑完但抽屉没有拉开。
- 逐种子结果见 [`results/heldout_seeds.csv`](results/heldout_seeds.csv)。

## 和官方公布的模型结果对比

Opus 5.5 和 GPT-6 Astra 的数字来自 ASPIRE 官方 README 里的图表（[`assets/official_libero_pro_by_model.png`](assets/official_libero_pro_by_model.png)），这两个模型我没有自己重跑。

| 套件 | Claude Opus 5.5（官方） | GPT-6 Astra（官方） | GPT-6.1 terra（本次） |
|---|---|---|---|
| Object swap | 98.2% | 99.0% | 100%（task 0，50/50） |
| Goal swap | 98.0% | 98.2% | 50%（task 0，25/50） |

在 10 个 LIBERO-Pro 任务的平均成功率上，官方公布的 Opus 5.5 是 99%（约 $18/任务）。GPT-6 Astra 在图上约 94%，没有标出具体数值。参考 [`assets/official_success_vs_cost.png`](assets/official_success_vs_cost.png)。

这个对比只能粗看，原因有三点。

1. 官方数字是整个套件多个任务的平均值，本次每个套件只跑了一个任务。
2. 官方对比的是 GPT-6 Astra，本次用的是 GPT-6.1 terra，两者不是同一代模型。
3. 本次每个任务只跑了一轮，官方的运行次数和网络条件我不清楚。

goal_swap task 0 只有 50%，明显低于官方两个模型的套件平均值。这说明 6.1 terra 至少在这个抽屉任务上还有差距，但要判断它在整个套件上的水平，需要把套件里的其他任务也跑完。

## 这次运行是怎么做的

1. 子代理先观察一个初始场景，从零写出 `v00_initial.py`，不提供任何基线程序。
2. 在开发种子 51–65 上运行，读取每次调用的 trace（感知结果、运动状态、终止原因），定位失败原因后写下一版。每个失败模式最多 3 版，总共最多 8 版。
3. 选定最终版本后，先在未见种子 66–80 上检查，再在留出种子 1–50 上一次性评测，评测期间程序冻结不改。
4. 程序只能调用公开感知和运动 API，不能读仿真器内部状态，也不能硬编码物体坐标。两个任务都通过了 API 审计。
5. 我核对了 Codex 的全部工具调用记录，它没有打开过仓库 `examples/` 下的官方示例程序。

## object_swap task 0 为什么前三版失败

LIBERO-Pro 的 object_swap 把目标物体换成了另一种外观。指令里还是写着 "alphabet soup"，但场景里对应的罐头已经变成蓝色。

- v00 运动超时，15 个种子全部报错。
- v01 加上从当前位置重试，程序能跑完，但 0/15。
- v02 改了放置位置和松爪后的等待时间，还是 0/15。
- v03 只改了一行，把 `localize_object('alphabet soup can')` 换成 `localize_object('blue soup can')`，结果 15/15。

前三版的 SAM3 分割用 "alphabet soup can" 锁定的是红罐头（置信度 0.25），换成 "blue soup can" 后锁定蓝罐头（0.75）。抓取动作本身早就没问题了，失败原因是认错了物体。

视频 [`videos/object_swap0_v02_wrong_can_seed51.mp4`](videos/) 是 v02 抓错红罐的样子，[`videos/object_swap0_success_seed1.mp4`](videos/) 是 v03 成功的样子。

## goal_swap task 0 为什么只有一半

v00–v05 一直是 0/15。先是往中间把手下降时卡住，后来改成侧面接近，又遇到逆运动学和接触超时。v06 改成先用 cuRobo 规划一条绕过灶台的高位路线，再从侧面接近拉开，第一次做到 7/15。v07 缩短接近距离，反而 15 个全部规划失败。8 版预算用完后，最终选定 v06。

## 资源消耗

| 运行 | 墙钟时间 | 总 token | 其中缓存命中 | 输出 token |
|---|---|---|---|---|
| object_swap task 0 | 23 分 42 秒 | 16,424,298 | 16,207,232 | 22,350 |

goal_swap 和 spatial_swap 是放在同一轮里跑的，三任务这一轮在中断前总共用了 38,443,089 token（缓存命中 98.9%）。spatial_swap 和 object_swap task 1 还没跑完，等跑完再补充结果。

硬件为 AutoDL 上的单卡 RTX 4090。

## 局限

- 这里只有仿真结果，每个任务只跑了一轮 Codex，没有统计多次运行之间的方差。
- 同一个模型每次推理路径都可能不同。上一轮在网络不稳定时只跑到 v04，最后 0 成功。
- goal_swap 的未见检查只有 6/15，说明 v06 的泛化性有限。

## 目录

```
programs/object_swap_task0/   v00–v03、fix_code.py（=v03）、CHANGELOG.md、findings.md
programs/goal_swap_task0/     v00–v07、fix_code.py（=v06）、CHANGELOG.md、findings.md
results/heldout_seeds.csv     两个任务留出种子 1–50 的逐种子结果
videos/                       agentview 视角的成功与失败示例
```

## 许可

ASPIRE 由 NVIDIA 以 Apache License 2.0 发布。这里的程序是基于 ASPIRE 的公开 API 生成的，同样以 Apache-2.0 发布。LIBERO / LIBERO-Pro 的场景渲染遵循各自项目的许可。
