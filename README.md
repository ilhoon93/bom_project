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

- 웹소켓을 통한 실시간 통신

  - 출금 요청 <--> 수락, 거절

    - 출금요청 리스트 테이블에 쌓아뒀다가
    - 유저 접속시 메시지 발송

    ```java
    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception{
        System.out.println("그룹 웹소켓 연결:" + session);
        sessions.add(session);
        UserVO loginUser = getUser(session);
        String senderId = getId(session);
        userSessions.put(senderId, session); // 사용자의 아이디와 그에 해당하는 세션 매핑
        System.out.println(loginUser); // 접속한 유저
        
        // 접속한 사용자가 요청받은 출금 목록
        List<MoneyrequestVONoList> result = mrService.selectMrListByUser(loginUser.getUserNo());
        
        System.out.println(result):
        
        // 접속한 사용자에게 출금 요청 메시지 전송
        for(MoneyRequestVONoList mr : result){
            TextMessage msg = new TextMessage(mr.getTrcAccountNo() + "모임계좌에서 \n" +
                              mr.getTrcTitle() + "목적으로" + mr.getTrcDate() + "까지" +
                              mr.getTrcAmount() + "원을 출금요청하였습니다. \n\n 확인을 누르면 연결계좌에서 바로 출금됩니다." + mr.getTrcAccountNo() + "," + mr.getTrcAmount() + "," + mr.getTrcTitle());
            session.sendMessage(msg);
        }
    }
    ```

    

  - 친구 초대 <--> 수락, 거절

    - 유저가 온라인일 때만 소켓 연결, 메시지 전송

    ```java
    if ("invite".equals(cmd) && invitedUserSession != null) {
    	invitedUserSession.sendMessage(tmpMsg);
    }
    ```

    

  - 모임 채팅방

    - 유저의 채팅방 입장, 퇴장 기록전송
    - 모든 접속 유저에게 메시지 보내기

    ```java
    // 클라이언트와 연결 이후에 실행되는 메서드
    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
    	sessionList.add(session);
        Logger.info("{} 연결됨", session.getId());
        
        String senderId = getId(session);
        String senderName = getName(session);
        userSessions put(senderId, session);
        for(WebSocketSession sess : sessionList){
            sess.sendMessage(new TextMessage(senderName + "님이 접속했습니다."));
            
        }
    }
    
    //클라이언트가 서버로 메시지를 전송했을 때 실행되는 메서드
    @Override 
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception{
        Logger.info("{}로 부터 {} 받음", session.getId(), message.getPayload());
        String senderName = getName(session);
        for (WebSocketSession sess : sessionList){
            sess.sendMessage(new TextMessage(senderName + " : " + message.getPayload()));
        }
    }
    ```

- Spring 트랜잭션 처리 어노테이션  `@Transactional`

  - pom.xml 추가

  ```xml
  <dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-tx</artifactId>
    <version>${org.springframework-version}</version>
  </dependency>
  ```

  - 서비스에 @Transactional 어노테이션 삽입후 DAO 부르기

  ```java
  @Transactional
  public void transferMoney(Map<String, Object> substractMoneyParam, Map<String, Object> addMoneyParam) {
  	moneyRequestDAO.updateSenderAccount(substractMoneyParam);
      moneyRequestDAO.updateRecieverAccount(addMoneyParam);
  }
  ```


- JSTL, MyBatis 사용법





## Quick Start

1. Clone the repo `git clone https://github.com/JinOokRhee/playground.git`
2. Go to your project folder from your terminal
3. Run: `npm install`
4. After install, run: `npm run start`
5. It will open your browser(http://localhost:3000)
