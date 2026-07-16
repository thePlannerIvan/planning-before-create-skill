# 验证与迭代

完成 Skill 前使用本文件。

## 目录

- [原则](#原则)
- [Eval Prompt 设计](#eval-prompt-设计)
- [五种失败模式扫描](#五种失败模式扫描)
- [Baseline 对比](#baseline-对比)
- [Forward Testing](#forward-testing)
- [Human Review](#human-review)
- [迭代规则](#迭代规则)
- [完成标准](#完成标准)

## 原则

验证要在实现前设计。一个 Skill 只有在目标失败模式上改变了模型行为，才算真的变好。

## Eval Prompt 设计

创建 2-5 个真实 prompt。它们应该像真实用户会说的话，而不是抽象测试句。

每个 eval 包含：

```json
{
  "id": "case-name",
  "prompt": "真实用户请求",
  "expected_behavior_change": "这个 Skill 应该让 agent 哪个行为变好",
  "files": [],
  "assertions": []
}
```

好的 eval 测试：

- 触发是否正确
- 是否遵守 workflow
- 是否读取正确 reference
- 是否使用正确 script/tool
- 是否在应停的人机介入点停下
- 是否完成 contract 交接
- 最终输出质量是否提升

## 五种失败模式扫描

验证阶段必须读取 `references/failure-modes.md`，检查：

- Premature Completion（过早完成）
- Duplication（重复）
- Sediment（沉积）
- Sprawl（蔓延）
- No-op（空操作）

这些不是泛泛质量问题，而是 Skill 结构问题。发现后优先修复对应层级：completion criterion、信息层级、resource 路由、contract、leading word 或 pruning。

## Baseline 对比

可行时比较：

- 新 Skill：without skill vs with skill
- 改进 Skill：old skill vs new skill

观察：

- 是否减少跳步
- 是否减少空泛结论
- 是否更好使用 references
- 是否有更好的中间产物
- 人机介入点是否更清晰
- 最终输出是否更稳定

## Forward Testing

可行时使用干净上下文。测试 agent 应收到：

- skill path
- task prompt
- input files
- output location

不要泄露：

- 预期答案
- 你的诊断
- 普通用户不会提供的隐藏成功标准

## Human Review

主观 Skill 中，人类 review 往往比纯定量断言更重要。

可以使用：

- 精简 prompt/output 摘要
- 并排对比
- checklist 评分
- 多输出 review 时使用反馈框

## 迭代规则

收到反馈后：

1. 判断失败属于 trigger、workflow、reference、script、contract、人机介入点，还是最终表达。
2. 用五种失败模式定位是否存在结构性问题。
3. 修复最小且持久的层。
4. 避免过拟合单个 eval prompt。
5. 重跑相关 eval。
6. 按 `references/continuous-iteration.md` 做目标 Skill 的持续迭代检查。

## 完成标准

一个 Skill 准备好，需要满足：

- 基础文件结构有效
- frontmatter 有 name 和 description
- references 能通过清晰 context pointer 找到
- 没有多余文档
- 代表性 eval 已运行，或已明确说明暂缓
- 残余风险已说明
