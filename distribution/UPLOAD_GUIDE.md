# 上传 NORM，让别人下载

固定公开下载页：
https://github.com/Lsofimeow/norm-website/releases/tag/windows-preview

1. 使用你的 GitHub 账号登录，打开上面的页面，点击铅笔图标 **Edit**。
2. 把实际可发布的 Windows 软件包命名为 **NORM_Preview_1.0.0.zip**，拖进 **Attach binaries** 区域，等上传完成。
3. 在发布说明中补充实际版本、使用说明、已知限制与校验值，点击 **Update release**。

官网的下载入口指向这个固定下载页。上传完成后，别人无需登录就能查看公开页面并下载该软件包。以后更新也使用同一个发布页面；保留文件名时，文件直链为：

https://github.com/Lsofimeow/norm-website/releases/download/windows-preview/NORM_Preview_1.0.0.zip

**当前附件已由你上传成功：NORM_Preview_1.0.0.zip，660,493,462 bytes。** 官网下载按钮已连接这个实际文件。软件运行未验证。GitHub 自动显示的 Source code 是网站源码，不能当作应用安装包。

以后上传新版本时，固定公开下载页保持不变。若附件使用了新的文件名，请同步更新 site.config.json 的 download_asset_url、installer_name、大小和校验值，才能让官网的直接下载按钮指向新文件。
