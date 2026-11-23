# 重玩《封神英傑傳》｜世嘉 MD 中文版

如果你记得蓝头发的林云、后来加入的燕蓉，还有山路上那场走格子的战斗，这份指南就是给你的。这里记录的是川普科技 1996 年的 Mega Drive 繁体中文版。搜索时也常写作《封神英杰传》，英文发行版叫 *Canon — Legend of the New Gods*，另有同名《曹操传》MOD。

本仓库提供启动脚本、键盘配置和验证方法。请自行准备合法取得的游戏镜像。使用 GitHub 网页的 **Code → Download ZIP** 下载本指南后，先解压到一个自己有写入权限的文件夹。

## 在 Windows 上开玩

1. 安装 Python 3.8 或更高版本。打开终端输入 `py -3 --version` 或 `python --version`，能显示版本即可。[Python 官方下载](https://www.python.org/downloads/windows/)
2. 从 RetroArch 官方下载页选择 Windows **Download (64bit)** 稳定便携包，解压后让 `RetroArch-Win64` 与 `Play.cmd` 并排。使用专门为这个游戏解压的一份，便于管理自己的配置。[RetroArch 下载页](https://www.retroarch.com/platforms.html) · [Windows 安装说明](https://docs.libretro.com/guides/install-windows/)
3. 在官方 Windows x64 核心目录下载 `genesis_plus_gx_libretro.dll.zip`，在 `RetroArch-Win64` 里新建 `cores` 文件夹（已有则沿用），把 ZIP 里的 DLL 解压到该文件夹。模拟器和核心都选 x64。[官方核心下载目录](https://buildbot.libretro.com/nightly/windows/x86_64/latest/) · [Genesis Plus GX 说明](https://docs.libretro.com/library/genesis_plus_gx/)
4. 在 `Play.cmd` 旁新建 `roms` 文件夹，把自己的游戏镜像解压放进去。支持此版本的裸镜像，文件名可以自定，后缀可用 `.md`、`.bin` 或 `.gen`。
5. 双击 **Play.cmd**。进入游戏画面后点一下窗口，按 **空格** 确认或推进剧情。战前选「出擊」，用 **←** 选「是」，再按空格。看到林云周围标出的移动范围，就可以用方向键选格子了。

```text
Play.cmd
play.py
fengshen.cfg
RetroArch-Win64/
  retroarch.exe
  cores/genesis_plus_gx_libretro.dll
roms/
  你自己的游戏镜像.md
```

### 按键与进度

| 要做的事 | 键盘 |
|---|---|
| 移动、选格子或菜单项 | ↑ ↓ ← → |
| 确认、推进对话（MD 的 A） | 空格 |
| 取消、返回（MD 的 B） | Delete |
| MD 的 C / Start | C / Enter |
| 打开或关闭模拟器快捷菜单 | F1 |
| 即时保存 / 读取当前槽 | F2 / F4 |
| 上一个 / 下一个存档槽 | F6 / F7 |
| 截图 / 切换快进 | F8 / Tab |

**第一次玩，先自己存一次。** 在林云可以行动时按 F2，等保存成功的提示出现。退出后重新打开，选回同一槽，按 F4 就能继续。F2 会覆盖当前槽，想保留关卡起点，可以按 F7 换槽，再存后续进度。笔记本的功能键可能需要配合 Fn。

战前菜单里的「儲存記錄」使用游戏本身的存档功能。脚本将这类存档放在 `runtime/saves/`，F2 的即时存档放在 `runtime/states/`。模板默认手动存、手动读。换电脑或重新解压指南前，正常退出模拟器，备份这两个文件夹。修改按键请编辑根目录的 `fengshen.cfg`，重新启动后生效。

## 核对自己找到的版本

脚本按大小和 SHA-256 识别这一个已验证的台湾版本。校验失败时先检查是否已解压；不同转储、交错式 SMD 镜像、翻译版和修改版可能有不同的指纹。请保留自己的原文件。

| 项目 | 此案例使用的镜像 |
|---|---|
| 数据库条目 | Feng Shen Yingjie Chuan (Taiwan)，MAME 条目 `fengshen` |
| 大小 | 2,097,152 字节 |
| SHA-256 | `870e1e55b356d76adf95c50dcafc52021572293224ab537217f9842ccba2fc85` |

游戏里还可以核对繁体「林雲」、职业「劍師」、初始等级 1 和移动力 4。[MAME 的 Mega Drive 卡带记录](https://github.com/mamedev/mame/blob/master/hash/megadriv.xml)

## 验证流程

在本指南目录打开终端。Windows 可用下面的命令；安装提供 `python` 命令的机器也可把 `py -3` 换成 `python`。

```powershell
py -3 play.py --check
py -3 play.py --verify
```

1. **文件核对。** `--check` 核对 ROM 指纹并检查模拟器和核心文件是否存在。架构兼容性要到实际加载时才能确认。
2. **画面核对。** `--verify` 单独启动模拟器，运行 900 帧后退出。每次测试在 `runtime/checks/` 下新建目录，终端打印日志和截图位置。打开 `opening.png`，看是否出现繁体开场剧情。这个步骤能检查实际渲染，人物操作需在游戏中验证。
3. **试玩与读档。** 正常启动，查看林云角色页，选择「出擊」。在第一场战斗用方向键选可达格子，空格确认进入行动菜单，Delete 返回。在一个空槽按 F2，退出重开，在同一槽按 F4，确认返回刚才的战场位置。

如果开场像在循环，先点击游戏窗口，尝试按空格推进；已有自己的即时存档时，可直接读回对应槽。如果日志出现 `An Application Control policy has blocked this file`，表示 Windows 在加载核心 DLL 时阻止了运行。在受管理的电脑上，请由设备管理员确认可用的核心版本。

## 其他系统或安装位置

启动脚本仅使用 Python 标准库。Linux 或 macOS 请安装对应平台的 RetroArch 及 Genesis Plus GX，用 `--retroarch` 和 `--core` 指定可执行文件与核心的实际路径，必要时用 `--rom` 指定镜像。路径含空格时加引号。以下参数适用于正常启动、`--check` 和 `--verify`。

```sh
python3 play.py --check --retroarch "/path/to/retroarch" --core "/path/to/genesis_plus_gx_libretro.so" --rom "/path/to/game.bin"
```

macOS 选择应用包内的可执行文件与本机安装的核心。2026-11-20 的 Windows x64 原始案例使用 RetroArch 1.22.2 与 Genesis Plus GX，实际看到了繁体林雲角色页、第一场战斗的移动范围，并验证了即时存档恢复。11 月 23 日复测公开脚本时，正常镜像校验通过，缺失及错误镜像均被识别；该设备的应用控制拦截了核心，本次未生成新的游戏截图。Linux 和 macOS 尚未实机验证。[RetroArch 命令行文档](https://docs.libretro.com/guides/cli-intro/)

本项目是玩家整理的非官方指南。仓库内原创脚本、配置及文字采用 MIT 许可；游戏、RetroArch 和模拟器核心分别归各自权利人所有。[本项目许可](LICENSE) · [RetroArch 许可](https://github.com/libretro/RetroArch/blob/master/COPYING) · [核心许可](https://github.com/libretro/Genesis-Plus-GX/blob/master/LICENSE.txt)
