<div align="center">

# 熵尾音 咬青 (Shang Wei Yin Kousei)

**双尾狼兽人声库 — 日语 CVVC 与 VCV 三声线 UTAU**

[![UTAU Voicebank](https://img.shields.io/badge/Platform-UTAU-7E9DBE?style=flat-square&logo=windows)](https://kuro-utau.heigao.me/)
[![Guide](https://img.shields.io/badge/Guide-V1.1-blue?style=flat-square)](Readme.txt)
[![Language](https://img.shields.io/badge/Language-JA_VCV&CVVC-orange?style=flat-square)](#-音源规格)
[![License](https://img.shields.io/badge/License-Custom-red?style=flat-square)](#-使用协议-usage-guidelines)
[![Website](https://img.shields.io/badge/Website-kuro--utau.heigao.me-brightgreen?style=flat-square)](https://kuro-utau.heigao.me)

</div>

---

## 🌐 官方主页

试听音轨、在线下载、完整协议等内容请访问官方网站：
[声库目录](https://kuro-utau.heigao.me/) · [进入熵尾音 咬青声库页](https://kuro-utau.heigao.me/kousei.html)

---

## 🎙️ 音源规格 (Voicebank Specs)

本音源收录三种声线，每种声线均以一个音高录制。推荐在 [OpenUtau](https://github.com/stakira/OpenUtau) 中配合 [HiFiUTAU](https://github.com/xiaobaijunya/HiFiUTAU-engine) 使用。

| 项目 | 规格 |
| :--- | :--- |
| 收录方式 | 日语 CVVC 与 VCV |
| 各声线录制音高 | 软声 B2、真声 B3、假声 B4 |
| 舒适音域 | D2–D6 |
| 推荐引擎 | `HiFiUTAU` |
| 声线特征 | 声音有力，唱起来透着一股自信。 |

### 💡 快速上手

1. 将下载的声库压缩包拖入 [OpenUTAU](https://github.com/stakira/OpenUtau) 窗口
2. 文本编码选 `utf-8`，歌手类型选 `utau`，按提示完成安装
3. 音轨中选择 `熵尾音 咬青`，引擎切换为 `HiFiUTAU` 即可开始编辑

---

## 🐺 角色设定 (Character Profile)

> 熵尾音来自宇宙，是某个未知存在的独立子体之一。容易打瞌睡，行动常由无意识驱动。面纹与双尾都是天生的，会随状态变化。特殊喜好是西瓜。

| 属性 | 设定 |
| :--- | :--- |
| 姓名 | 熵尾音 こうせい（熵尾音 咬青） |
| 种族 | 狼（兽人） |
| 性别 | 男性 |
| 年龄 | 约 17 岁 |
| 生日 | 8 月 14 日 |
| 身高 | 约 168 cm |
| 外观特征 | 面纹、双尾（随状态变化） |
| 喜好 | 西瓜 🍉 |

[简介、先天双尾与颈环式麦克风的完整设定](Readme.txt)

---

## 📥 下载 (Download)

以下为公开配布的 V1 下载入口。V1 对应的使用条款可查阅[官网 V1 协议](https://kuro-utau.heigao.me/assets/terms-v1.html#zh)。

| 平台 | 链接 |
| :--- | :--- |
| **GitHub Releases (V1)** | [前往下载](https://github.com/Heigao-Clank/kuro-voicebank/releases/tag/V1) |
| **Bowlroll** | 暂无下载链接 |
| **Google Drive** | [前往下载](https://drive.google.com/file/d/1WB_3wNww9CAy_1M7UDJVFeQKciWdL78O/view?usp=drive_link) |
| **123云盘** | [前往下载](https://1820313552.share.123pan.cn/123pan/TUtojv-ViaY) |

---

## ⚖️ 使用协议 (Usage Guidelines)

本地 V1.1 的完整协议、角色资料与常见问题见[中文](Readme.txt)、[English](Readme_EN.txt) 和 [日本語](Readme_JP.txt)。每版使用条件以[声库官网公布的对应版本](https://kuro-utau.heigao.me/kousei.html#guidelines)为准。

---

## 官网构建与验收

总首页 `index.html` 使用唱片架样式 `assets/catalog.css`。咬青的夜蓝专页使用 `kousei.html`（中文）、`index-en.html`（英语）和 `index-jp.html`（日语）。专页与历史协议页共用 `style.css`，专页的手机首屏布局在 `assets/mobile-cover.css`。更新 `kousei.html`、三语文案或指南后，在项目根目录运行：

```sh
python3 scripts/build-locales.py
python3 scripts/build-locales.py --check
```

第一条命令生成三语静态页面，第二条核对生成结果。项目根目录的总首页、三语专页、样式、`assets/`、`font/` 和 `favicon.ico` 可直接用于静态托管。

浏览器回归检查覆盖手机导航、协议打印、无 JavaScript 下载和试听失败后的重试。开发环境安装 Playwright 及 Chromium 后运行 `node scripts/check-site.cjs`。也可传入以斜杠结尾的本地预览网址；使用已安装的 Chrome 时可通过 `CHROME_PATH` 指定可执行文件。

---

## 📬 联系方式 (Contact)

作者 **黑篙 (Heigao)**：

* 📧 [heigao75@qq.com](mailto:heigao75@qq.com)
* 🐦 [@heigao_tickle](https://twitter.com/heigao_tickle)
* 📺 [Bilibili 黑篙](https://space.bilibili.com/695724697)
* 🌐 [heigao.me](https://heigao.me)

---

<div align="center">
  <p>© 2026 黑篙 (Heigao). All Rights Reserved.</p>
</div>
