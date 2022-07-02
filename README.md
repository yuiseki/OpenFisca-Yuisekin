# OpenFisca Yuisekin

## 開発参加方法

### 前提

- https://scrapbox.io/c4j/GitHubでの共同開発への参加の準備
  - GitHub にユーザー登録する
  - GitHub Desktop または Git コマンド をセットアップする
  - Visual Studio Code をセットアップする

## このリポジトリを GitHub であなたのアカウントへ Fork して、 `git clone` する

## Fork したあなたのリポジトリで、GitHub Codespaces を起動して、Visual Studio Code で開く

[![Image from Gyazo](https://i.gyazo.com/a29c4cce16baca1b33978231849b2269.png)](https://gyazo.com/a29c4cce16baca1b33978231849b2269)
[![Image from Gyazo](https://i.gyazo.com/1351c39a5ac9a4f5a4a4ae9901ec12d6.png)](https://gyazo.com/1351c39a5ac9a4f5a4a4ae9901ec12d6)

### GitHub Codespaces で動作確認する

```
make
```

## GitHub Codespaces で API サーバーとして動かす

```
make serve-local
```

- GET http://localhost:5000/spec
- GET http://localhost:5000/entities
- GET http://localhost:5000/variables
- GET http://localhost:5000/parameters
