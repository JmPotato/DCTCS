# DCTCS

A distributed central temperature control system.

一个分布式中央温控系统。

## Development Notice 开发须知

本分支为 dev 分支，区别于 master 主分支，有如下区别：

- 代码合入标准更低，以快速迭代为主
- 改动幅度和频率更大

当一个主要功能实现或更新完毕时，方可将代码合入 master 分支。

开发的最佳实践如下，希望各位都能遵守。首先，将远程分支 `clone` 到本地，然后切换到 dev 分支。

```shell
# 也可以使用 git clone https://github.com/JmPotato/DCTCS.git
git clone git@github.com:JmPotato/DCTCS.git
# 确保分支信息与远端同步
git fetch --all
# 切换分支
git checkout dev
```

每次开发前，确保执行一次 `pull`，保证远程分支与本地同步，避免之后 `push` 时产生冲突。

```shell
git pull origin dev
# 做了一些改动，add 并 commit 之后
git push origin dev
```

具体 Git 使用教程，可以参考 [《Pro Git》](https://www.progit.cn/)。

## Usage 使用方法

项目根目录下运行 `make run-backend-dev` 即可运行后端 server，默认访问地址为 http://localhost:5000