# 五种失败模式

本文件来自 `writing-great-skills` 的核心思想，用于创建、验证或重构 Skill 时做最后扫描。

## 目录

- [使用时机](#使用时机)
- [1. Premature Completion（过早完成）](#1-premature-completion过早完成)
- [2. Duplication（重复）](#2-duplication重复)
- [3. Sediment（沉积）](#3-sediment沉积)
- [4. Sprawl（蔓延）](#4-sprawl蔓延)
- [5. No-op（空操作）](#5-no-op空操作)
- [最终扫描模板](#最终扫描模板)

## 使用时机

在这些阶段必须使用：

- workflow map 完成后：检查流程设计是否会诱发失败。
- 目标 `SKILL.md` 写完后：检查文本结构和信息层级。
- references/scripts/assets 放置完成后：检查是否有重复、沉积或蔓延。
- eval 或用户反馈暴露问题后：定位失败属于哪一类。

## 1. Premature Completion（过早完成）

含义：agent 在步骤真正完成前就宣布完成，注意力从“把当前步骤做透”滑向“赶紧进入下一步”。

常见信号：

- completion criterion 模糊，比如“整理好”“分析充分”。
- 当前步骤能看到太多后续步骤，产生抢跑。
- 没有文件关隘或 contract，导致下游无法检查上游是否真的完成。
- agent 输出结论，但没有证据文件、中间产物或检查记录。

防御方式：

- 优先收紧 completion criterion，让它可检查。
- 给每一步明确输出文件和 contract。
- 对高风险步骤使用 L2 文件关隘、L5 合约或 L4 拆分 Agent。
- 如果后续步骤会诱发抢跑，把后续步骤隐藏到子 Agent 或后续 reference。

检查问题：

```text
□ 每一步是否有可检查的完成标准？
□ 是否有步骤只靠“模型觉得完成了”？
□ 是否有当前步骤能看到过多后续步骤？
□ 是否需要文件关隘、合约或拆分 Agent？
```

## 2. Duplication（重复）

含义：同一含义出现在多个地方。重复会浪费上下文、增加维护成本，并让某个含义被过度放大。

常见信号：

- description 里多个触发短语其实是同一个分支。
- `SKILL.md` 和 reference 文件重复解释同一规则。
- 同一个 contract 字段在多个文件里有不同说法。
- 多个 scripts 做相近事情但命名不同。

防御方式：

- 保持 single source of truth。
- description 中一个分支只写一次。
- 把详细解释放到 reference，`SKILL.md` 只保留 pointer。
- 重复描述如果只是为了强化语感，考虑坍缩成 leading word。

检查问题：

```text
□ 同一规则是否出现多次？
□ description 是否堆叠同义触发词？
□ SKILL.md 是否重复了 reference 中的细节？
□ 是否能用一个 leading word 替代多处重复描述？
```

## 3. Sediment（沉积）

含义：旧版本、临时规则、过期经验沉积在 Skill 中，因为添加容易、删除困难。

常见信号：

- references 中有旧流程但没人再读。
- scripts/assets 是早期实验残留。
- memory 里的经验已失效，但还影响当前流程。
- `SKILL.md` 里有“以防万一”的旧限制。

防御方式：

- 每次大改后删除不用的资源。
- Memory Audit 时判断：写 memory、升级 Skill，还是删除。
- 只保留直接服务当前 workflow 的资源。
- 对过期经验标记并移除活跃路径。

检查问题：

```text
□ 是否有无路由的 reference？
□ 是否有不再调用的 script 或 asset？
□ 是否有旧规则与新 workflow 冲突？
□ 是否有“临时加的”内容已经变成永久负担？
```

## 4. Sprawl（蔓延）

含义：Skill 太长、太散，即使每一行看起来都有用，整体也会损害可读性和上下文效率。

常见信号：

- `SKILL.md` 过长，包含多个分支的细节。
- 所有任务都被迫加载只在某个分支需要的知识。
- reference 文件没有清晰路由。
- 一个 Skill 同时承担多个应独立触发的 leading word。

防御方式：

- `SKILL.md` 只保留所有路径都需要的流程和路由。
- 分支细节下沉到 reference。
- 大 reference 按领域、步骤或变体拆分。
- 如果有独立触发词和独立 workflow，考虑拆 Skill 或做 router。

检查问题：

```text
□ SKILL.md 是否只包含所有路径都需要的内容？
□ 是否有分支内容被所有运行强制加载？
□ reference 是否按需读取，而不是一上来全读？
□ 是否应该拆成多个 Skill 或一个 router Skill？
```

## 5. No-op（空操作）

含义：某行指令没有改变模型默认行为，却消耗上下文。

常见信号：

- “认真一点”“要全面”“请保持专业”等弱指令。
- 只是重申模型本来会做的事。
- 指令没有检查方式，也没有改变流程。
- 加了很多形容词，但没有具体行为变化。

防御方式：

- 对每句话做 no-op test：删掉它，行为会变吗？
- 把弱词换成强 leading word，或换成可执行动作。
- 用 checklist、contract、script、文件关隘替代泛泛要求。
- 删除不会改变行为的句子。

检查问题：

```text
□ 这句话删掉后，agent 行为会不会一样？
□ 是否有泛泛形容词，没有具体动作？
□ 是否能改成文件、contract、script 或 checklist？
□ 是否能用更强的 leading word 锚定行为？
```

## 最终扫描模板

在完成 Skill 前，输出或内部检查：

```text
Failure Mode Scan
- Premature Completion: [通过/风险/修复]
- Duplication: [通过/风险/修复]
- Sediment: [通过/风险/修复]
- Sprawl: [通过/风险/修复]
- No-op: [通过/风险/修复]
```

如果发现风险，优先修复；如果暂不修复，在最终回复中列为残余风险。
