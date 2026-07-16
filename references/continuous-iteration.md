# 持续迭代机制

本文件用于把 Memory 和反馈机制写进每一个被创建出来的目标 Skill。

## 核心语义

Memory 不是本规划 Skill 的一次性收尾动作，而是目标 Skill 的长期自我改进机制。

创建任何目标 Skill 时，都要让它包含一套运行后的持续迭代规则：

- 本次运行中哪些纠正会影响下次？
- 哪些反馈只属于当前任务？
- 哪些经验要写入 memory？
- 哪些问题应该升级进 `SKILL.md`、references、contracts、scripts 或 assets？
- 哪些旧内容应该删除，避免沉积？

## 目标 Skill 中必须出现的内容

在目标 Skill 的 `SKILL.md` 或合适 reference 中加入一个“运行后迭代”小节。保持精简，但必须说明：

```markdown
## 运行后迭代

每次使用本 Skill 后，做一次 Memory Audit：

1. 只影响当前任务的过程记录，不写入 memory。
2. 会影响同项目下次运行的用户偏好、数据源限制、项目约束，写入 project memory。
3. 会影响本 Skill 某一步的经验，写入 step memory candidate。
4. 连续出现或已确认通用的问题，升级到 SKILL.md、references、contracts、scripts 或 assets。
5. 已失效的旧规则、旧资源、旧 memory，标记并移除活跃路径。
```

## 升级路径

| 发现 | 去向 |
|---|---|
| 用户个人偏好 | project/user memory |
| 项目特定配置 | project memory |
| 某一步偶发经验 | step memory candidate |
| 连续出现的流程缺陷 | `SKILL.md` 或 `references/workflow/` |
| 合约漏检查项 | `references/contracts/` |
| 重复手工操作 | `scripts/` |
| 触发不准确 | frontmatter `description` |
| 旧规则不再适用 | 删除或移出活跃路径 |

## 运行后提问方式

不要每次都输出大段总结。使用轻量、高信号的提示：

```text
这次运行有 2 个可能值得记住的点：
1. [只在下次会改变行为的经验]
2. [可能需要升级到 Skill 的问题]

你希望我：
A. 写入项目 memory
B. 作为 Skill 改进候选
C. 忽略
```

## 完成标准

目标 Skill 完成前必须检查：

```text
□ 是否说明了运行后 Memory Audit？
□ 是否区分 memory、Skill 升级和忽略？
□ 是否说明用户确认后再写长期 memory？
□ 是否有防止 sediment 的删除/失效机制？
□ 是否把持续迭代机制放在合适层级，而不是塞进每一步正文？
```
