# Beauty Opinion Mining

**프로젝트설명** : 후기에 민감함 뷰티 제품들의 리뷰 데이터를 분석해 고객 관리, 마케팅을 도와주는 웹 플랫폼

**프로젝트 기간** : 2018-03 ~ 2018-06 (약 3개월)

**프로젝트목적** : 팀프로젝트 (캡스톤 디자인 최종결과물)

**역할** : 백엔드 개발, 리뷰 크롤링 프로그램 개발, 배포

**개발환경**

- **FrontEnd** : react, JavaScript, html/css
- **Backend** : python, Django, MongoDB
- **DataAnalysis** : tensorflow, gensim
- **Server** : AWS



![](https://github.com/ilhoon93/imageHub/blob/master/img/reduction-admin.jpg?raw=true)











## 시스템 구조
- **전체 시스템 구조도**

  ![](https://github.com/ilhoon93/imageHub/blob/master/img/%EC%8B%9C%EC%8A%A4%ED%85%9C%EA%B5%AC%EC%A1%B0%EB%8F%84.JPG?raw=true)



- **데이터 수집 프로세스**

  ![](https://github.com/ilhoon93/imageHub/blob/master/img/%ED%81%AC%EB%A1%A4%EB%A7%81%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4.JPG?raw=true)





## 주요 기능

1. 실시간 크롤링

```
- 미미박스, 글로우픽, 화해, 메이크업앨리, 오픈마켓 데이터 등등 다양한 사이트의 리뷰 실시간 수집
```

2. 데이터 분석 결과 그래프 제공

```
- 리뷰 텍스트 및 기타 데이터를 다양하게 분석하여 마케팅에 활용가능한 분석 결과 제공
- 3p전략, 시장 세분화, 워드클라우드, 포지셔닝 맵 등
```

3. 감성 점수 변화에 따른 알림

```
- 구축한 감성 모델에 따른 점수를 기반으로 제품에 대한 점수가 일정 기준 이하로 떨어지면 알림 제공
```





## 프로젝트를 통해 배운 점




## Quick Start

1. Clone the repo `git clone https://github.com/JinOokRhee/playground.git`
2. Go to your project folder from your terminal
3. Run: `npm install`
4. After install, run: `npm run start`
5. It will open your browser(http://localhost:3000)
