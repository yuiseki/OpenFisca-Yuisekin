# OpenFisca Yuisekin

## 開発参加方法

### 前提

- https://scrapbox.io/c4j/GitHubでの共同開発への参加の準備
  - GitHub にユーザー登録する
  - GitHub Desktop または Git コマンド をセットアップする
  - Docker をセットアップする

### リポジトリを GitHub で自分のアカウントへ Fork して、 `git clone` する

#### GitHub Desktop をセットアップしている場合

- GitHub Desktop で「OpenFisca-Yuisekin」を Clone する

#### Git コマンドをセットアップしている場合

```
git clone git@github.com:あなたのGitHubユーザー名/OpenFisca-Yuisekin.git
cd OpenFisca-Yuisekin
```

### Docker イメージをビルドする

```
docker compose build
```

### テストを実行する

```
docker compose run --rm openfisca /bin/bash -c "make build && make test" 
```

## API サーバーとして動かす

```
docker compose up
```

- GET http://localhost:5000/spec
- GET http://localhost:5000/entities
- GET http://localhost:5000/variables
- GET http://localhost:5000/parameters
