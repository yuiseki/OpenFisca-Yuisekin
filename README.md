# OpenFisca Yuisekin

## 開発参加方法

### Docker をセットアップする

### リポジトリを `git clone` する

```
git clone git@github.com:yuiseki/OpenFisca-Yuisekin.git
cd OpenFisca-Yuisekin
```

### Docker をビルドする

```
docker compose build
```

### テストを実行する

```
docker compose run --rm openfisca make test
```

## API サーバーとして動かす

```
docker compose up
```

http://localhost:5000/
