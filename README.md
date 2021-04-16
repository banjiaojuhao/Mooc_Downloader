源项目好像是支持很多平台的，但是很多平台都没有开源。源项目已经停止更新，这个fork修修bug。有问题可以邮箱求助。

现在支持的平台很少，只有icourse和icouse163

运行项目：python -m Mooc

# 修改内容
- 移除下载速度限制
- 修复host错误造成的下载失败
- 添加自定义cookie支持
- 添加对m3u8格式支持（需要将ffmpeg添加进PATH）

# todo
- m3u8下载加速（自己下载后用ffmpeg合并）
- rust重写项目
