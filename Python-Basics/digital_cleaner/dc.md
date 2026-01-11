# 文件整理助手
主要功能：根据文件后缀，将文件整理到对对应类型的文件夹里
## 文件后缀类型
- Image 
    jpg, jpeg, png, gif, webp, svg, psd, raw
- Document
    txt, md, pdf, docx, xlsx, pptx, csv, log
- Audio
    mp3, wav, flac, aac, ogg, wma, m4a, opus, mid, ape
- Video
    mp4, mkv, mov, avi, wmv, flv, webm, m4v, rmvb, ts
- Code
    c, cpp, py, java, js, ts, html, css, php, go, rs, sh, bat, ps1
- Data
    json, yaml, yml, xml, sql, csv, nbt, dat, db, sqlite
- Archive
    zip, rar, 7z, tar, gz, bz2, xz
- Executable
    exe, msi, bat, sh, dll, sys, iso, com, bin, deb, rpm, jar
- Specialized
    litematic, schem, ttf, otf, cur
- Others

## 功能细节
- 原始路径：可以选择单个或者多个（未实现）原始路径，处理根目录的所有文件（略过文件夹）
- 目标路近：整理出来的文件夹放入选择的单个目标路径
- 文件后缀黑名单（未实现）
- 文件后缀白名单（未实现）
- 撤销功能（逻辑不完整，谨慎使用）

## 文件架构
```
|-- __init__.py
|-- data/log.json
|-- core/classifier.py
|-- models/file.py
|-- utils/history.py
|-- main.py
```
## 重构待办 
- [ ] **撤回逻辑升级**：引入 `Batch ID` (批次号)，实现按操作批次精准撤回；修正为倒序遍历 (LIFO)。
- [ ] **魔数识别 (Magic Number)**：增加二进制文件头读取逻辑，通过十六进制特征码识别真实文件类型（防后缀伪装）。
- [ ] **性能与规范**：将日志加载移出主循环；修正 `main_muen` 拼写错误；统一使用 `FileItem` 类方法拼接路径。
- [ ] **功能补全**：实现多源路径输入；添加后缀黑/白名单过滤；增加基于 Hash 的文件去重/重命名策略。