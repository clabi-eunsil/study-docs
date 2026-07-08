# MLOps Study Docs

MLOps 관련 학습 내용을 정리한 문서 모음이다.   
각 study repo에 commit되는 내용을 바탕으로 이 사이트가 자동으로 갱신된다.

## 처음이신가요?

각 챕터는 개념 설명이 먼저 나오고,
실습 코드는 본문 중간에 접힌 상태(▶)로 들어가 있어서 펼쳐보지 않고 그냥 읽고
넘어갈 수 있다. 실습을 직접 따라 해보고 싶을 때만 [실습 환경 구성 가이드](getting-started.md)를
보면 된다 — 안 봐도 문서를 읽는 데는 지장이 없다.

모르는 용어가 나오면 아래 용어집에서 찾아본다.

- [Model Serving 용어집](model-serving/GLOSSARY.md) — 카테고리·태그로 정리된 전체 용어
- [Kubeflow 용어집](kubeflow/GLOSSARY.md)

## 주제

- [Model Serving](model-serving/README.md) — 모델 서빙 기본 개념부터 vLLM, Docker, Kubernetes, KServe 배포까지
- [Kubeflow](kubeflow/README.md) — Kubeflow 컴포넌트별 실습 로드맵 (진행 중)

## 스터디 방법

여기 정리된 문서는 원본 study repo의 내용을 빌드 시점에 가져온 것이다.
읽기만 할 목적이면 이 사이트 안에서 전부 해결된다.

스크립트를 직접 돌려보고 싶을 때만 원본 repo를 clone해서 실행해볼 수 있다.
clone부터 챕터별 실행 환경(`.venv`, Docker, Kubernetes) 구성까지 단계별로 정리한
[실습 환경 구성 가이드](getting-started.md)를 참고한다.

## 기여하기
오탈자, 개선 내용이 있을 때에는 Issue나 PR을 직접 생성하여 직접 기여할 수 있다.