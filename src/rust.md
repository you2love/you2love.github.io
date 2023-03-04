---
# Rust
---

* [官网](https://www.rust-lang.org/)

```sh
Rustup metadata and toolchains will be installed into the Rustup
home directory, located at:

$HOME/.rustup

This can be modified with the RUSTUP_HOME environment variable.

The Cargo home directory located at:

  $HOME/.cargo

This can be modified with the CARGO_HOME environment variable.

The cargo, rustc, rustup and other commands will be added to
Cargo s bin directory, located at:

  $HOME/.cargo/bin

This path will then be added to your PATH environment variable by
modifying the profile files located at:

  $HOME/.profile
  $HOME/.bashrc
  $HOME/.zshenv

You can uninstall at any time with rustup self uninstall and
these changes will be reverted.
```

* [中文官网](https://www.rust-lang.org/zh-CN)

* [rocket-web框架](https://rocket.rs/)

* 小知识
  * 升级rust及相关工具链

  ```shell
  rustup update
  ```

  * 本地查看文档

  ```shell
  rustup doc
  ```

  * 每隔一段时间就发布一个版次,主要有2015,2018,2021,主程序和库代码可以依赖不同版次的.

* [强大的rust的web框架](https://salvo.rs/)

### mdbook-快速安心写书

* 安装

```bash
cargo install mdbook
cargo install mdbook-pdf
cargo install mdbook-mermaid
cargo install mdbook-toc
```
