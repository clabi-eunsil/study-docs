# 실습 환경 구성

이 사이트는 문서만 모아서 보여주고, 실제 실습(스크립트 실행, 배포)은 각 study repo를 clone해서
로컬 또는 원격 GPU 서버에서 진행한다.

## 공통 준비물

- git, Python 3.10+ (python3, pip)
- 일부 챕터에 한해: Docker, kubectl + Kubernetes 클러스터(예: minikube), NVIDIA GPU 드라이버와 NVIDIA Container Toolkit — 어떤 챕터에 필요한지는 그 챕터 페이지 상단에 안내되어 있다

## 1. repo clone

```bash
git clone https://github.com/clabi-eunsil/model-serving-study.git
cd model-serving-study
```

## 2. 챕터별 실행 환경 구성

### Python 스크립트를 직접 실행하는 챕터

챕터마다 필요한 패키지와 버전이 다를 수 있어서, 공용 가상환경을 쓰지 않고 챕터 폴더 안에
독립된 `.venv`를 만든다.

```bash
cd chapters/02-fastapi-serving
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

실습이 끝나면 가상환경에서 나온다.

```bash
deactivate
```

### Docker / Kubernetes / KServe 챕터

실행 환경이 container나 cluster 안에 있는 챕터는 host에 `.venv`를 만들 필요가 없다.
대신 해당 챕터 README에 안내된 `docker build` / `docker compose up`, `kubectl apply` 같은
명령을 그대로 따라가면 된다. (예: NVIDIA Container Toolkit이 필요한 GPU container, NGC API key가
필요한 NIM, minikube/kubectl이 필요한 Kubernetes·KServe 챕터)

## 3. 정확한 실행 명령은 각 챕터 페이지에

필요한 API key(NGC, Hugging Face 등), GPU 요구사항, 정확한 실행 순서는 각 챕터 페이지 상단에
정리되어 있다. 실습을 시작하기 전에 해당 챕터를 먼저 읽는다.

## 기여하기

실습하다가 오탈자나 개선할 내용을 발견하면 원본 repo에 Issue를 남기거나, 직접 고쳐서 PR을 보내면 된다.

- [model-serving-study](https://github.com/clabi-eunsil/model-serving-study)
