# OpenFisca Yuisekin

## 開発参加方法

### 前提

- GitHub にユーザー登録する
- Visual Studio Code をセットアップする

### 概要

- （このリポジトリ を自分の GitHub アカウントに Fork する | 既に Fork してる場合は Fetch upstream する（必須））
- → Fork した自分のアカウントの側のリポジトリをブラウザで開き、緑色の「Code」ボタンをクリック
- → 「Create codespace on main」をクリック
- → 「Open this codespace in VS Code Desktop」をクリック
- → ダイアログが数回表示されるので全部 OK っぽい方をクリック
- → VSCode と GitHub を連携させるために認証が求められるので承認する
- → VSCode で GitHub Codespaces に無事に接続できたら、動作確認のために、ターミナルで `make` を実行

これだけで全員同じ環境で開発できるようになるはず。料金は 2022-07-02 現在、無料です。

### このリポジトリを GitHub であなたのアカウントへ Fork して、 `git clone` する

### Fork したあなたのリポジトリで、GitHub Codespaces を起動して、Visual Studio Code で開く

[![Image from Gyazo](https://i.gyazo.com/a29c4cce16baca1b33978231849b2269.png)](https://gyazo.com/a29c4cce16baca1b33978231849b2269)
[![Image from Gyazo](https://i.gyazo.com/1351c39a5ac9a4f5a4a4ae9901ec12d6.png)](https://gyazo.com/1351c39a5ac9a4f5a4a4ae9901ec12d6)

### GitHub Codespaces で動作確認する

```
make
```

### GitHub Codespaces で API サーバーとして動かす

```
make serve-local
```

- GET http://localhost:5000/spec
- GET http://localhost:5000/entities
- GET http://localhost:5000/variables
- GET http://localhost:5000/parameters
