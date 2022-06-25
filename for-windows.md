# OpenFisca Windows向けの情報まとめ

## 環境構築のすすめ

### 前提

- https://scrapbox.io/c4j/GitHubでの共同開発への参加の準備
  - Git をセットアップする
  - GitHub にユーザー登録する
  - Docker をセットアップする

### リポジトリをForkする

GitHubのこのリポジトリをforkする

### forkしたリポジトリをCloneする

```
git clone git@github.com:<あなたのGitHub ユーザーネーム>/OpenFisca-Yuisekin.git
```

### 環境変数を利用してPythonにUTF-8を強制させる
Powershellを起動し以下のコマンドを入力して下さい。

```
$env:PYTHONUTF8=1  
```

## テストの実行

openfiscaのディレクトリに移動し、以下のコマンドを実行
```
docker compose run --rm openfisca /bin/bash -c "make build && make test"
```