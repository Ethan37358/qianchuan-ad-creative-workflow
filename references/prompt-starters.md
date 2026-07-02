# Prompt Starters

Use this when the user invokes the skill without enough product information.

## Standard First Reply

Send this form and ask the user to fill what they know:

```text
模式：全自动 / 半自动
素材来源：本地 / 网络采集 / 本地优先+网络补充
配音方式：MiniMax / 真人录音 / 暂不配音
是否加BGM：是 / 否
视频数量：1条 / 3条 / 批量
视频时长：15秒 / 30秒 / 45秒

商品/类目：
价格/优惠：
投放目标：商品卡成交 / 直播间引流 / 线索 / 复购
目标人群：
核心卖点：
真实证据：
使用场景：
已有素材路径：
禁用表达：
期望风格：
参考素材/竞品：
补充说明：
```

## If User Wants Full Auto

Add this warning:

```text
全自动会直接生成粗剪视频，但仍需要你最终审核商品事实、授权、合规和素材观感。
```

## If User Wants Semi Auto

Explain gates:

```text
半自动会在创意方向、口播、素材候选、粗剪成片这几个节点停下来让你确认。
```

## If Keys Are Missing

Do not block planning. Say:

```text
缺少 API key 不影响创意、口播、分镜和本地素材规划；只会影响网络素材采集或 MiniMax 配音。
```

Then proceed as far as possible.

